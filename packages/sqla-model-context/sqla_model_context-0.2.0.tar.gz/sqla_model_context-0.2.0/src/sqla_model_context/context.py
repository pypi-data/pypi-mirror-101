import contextlib
import enum
import logging
import warnings
from collections import deque
from typing import Any
from typing import Callable
from typing import Deque
from typing import Dict
from typing import Generic
from typing import Iterator
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from sqlalchemy import event
from werkzeug.local import LocalProxy

from .exc import ContextRelationListenerWarning
from .exc import MissingRelation
from .exc import NoActiveRelation

M = TypeVar("M")
#: The target model

R = TypeVar("R")
#: The related model


class EnforceMode(enum.Enum):
    """Determines how to enforce relationships at insert time."""

    NONE = enum.auto()
    #: No enforcement of relationships.

    LOG = enum.auto()
    #: Send a log message when relationship is missing.

    WARN = enum.auto()
    #: Send a log warning when relationship is missing.

    ERROR = enum.auto()
    #: Raise an error when the relationship is missing.

    @classmethod
    def parse_arg(cls, value: Union[str, bool, "EnforceMode"]) -> "EnforceMode":
        """Parse an arguemtn into the enforcement mode enum. Possible values are:

        * A boolean, where `True` means `ERROR`, i.e. do enforcement and raise an error,
          and `False` means do nothing (`NONE`)
        * A string which corresponds to one of the enumerations.
        * An actual enumeration value

        This method always returns an enumeration value, or raises an error.
        """

        if isinstance(value, bool):
            return EnforceMode.ERROR if value else EnforceMode.NONE
        if isinstance(value, str):
            return EnforceMode[value]
        return value


class ModelRelativeContextManager(Generic[M, R]):
    """A context manager to provide default values for a relationship property.

    Using SQLAlchemy events, intercept the creation of model objects, and ensure that those objects
    have an appropriate relationship set. The `enforce` keyword also provides a check during the
    `before_insert` that the relationship property was set.

    A `default_value` function can also be provided as a fallback. When the `default_value` is provided, it should
    return the correct default relationship entity in the current context.

    This context manager assumes that the relationship on the target class is handled as a keyword argument during the
    __init__ method of the target instance, and that the foriegn key can also be detected as a keyword argument.

    Parameters
    ----------
    basecls: type
        The type used to filter events - can be a base class or mixin, which has the approprite
        relationship properties.
    relationship_attr: str
        The name of the relationship property on the model class. This is _not_ the underlying column
        but the actual relationship property where the related object can be found.
    fk_attr: str
        The name of the foreign key on the target model - used to identify when an explicit identifier
        has been passed to `__init__`. Defaults to `relation_name_id` for `relation_name`.
    enforce: bool
        When true (default), this relationship be enforced to be not-null during the insert event.
    default_value: callable
        A no-argument function which returns the appropriate default value for this context, which can
        be applied to target objects as `relationship_attr`.

    """

    def __init__(
        self,
        basecls: Type[M],
        relationship_attr: str,
        fk_attr: Optional[str] = None,
        enforce: Union[bool, str, EnforceMode] = True,
        default_value: Optional[Callable[[], R]] = None,
        logger: Optional[str] = None,
        listen: bool = True,
    ) -> None:

        self.basecls = basecls
        self.relationship_attr = relationship_attr
        self.fk_attr = fk_attr or f"{relationship_attr}_id"
        self.default_value = default_value
        self.enforce = EnforceMode.parse_arg(enforce)
        self._stack: Deque[R] = deque([])
        self.logger = logging.getLogger(logger or basecls.__module__)
        self._listening = False

        if listen:
            self._init_listeners()

    def _init_listeners(self) -> None:
        if self._listening:
            warnings.warn(ContextRelationListenerWarning("{self!r} applied listeners multiple times."))
        # TODO: Why is propagate=True important here?
        event.listen(self.basecls, "init", self._init_ensure_relation, propagate=True)
        if self.enforce != EnforceMode.NONE:
            event.listen(self.basecls, "before_insert", self._insert_check_relation, propagate=True)
        self._listening = True

    def _remove_listeners(self) -> None:
        event.remove(self.basecls, "init", self._init_ensure_relation)
        if self.enforce != EnforceMode.NONE:
            event.remove(self.basecls, "before_insert", self._insert_check_relation)
        self._listening = False

    @contextlib.contextmanager
    def listen(self) -> Iterator["ModelRelativeContextManager"]:
        self._init_listeners()
        try:
            yield self
        finally:
            self._remove_listeners()

    def __repr__(self) -> str:
        # TODO: Expose additional attributes here?
        return (
            f"ModelRelativeContextManager({self.basecls.__name__}.{self.relationship_attr} enforce={self.enforce.name})"
        )

    def _check_instance(self, target: M) -> bool:
        """
        Check that this target instance is appropriate for this relationship.

        Useful if the baseclass provided was too broad and the relationship property doesn't actually exist.

        Parameters
        ----------
        target: instance of M
            The model instance being targeted by this context.

        Returns
        -------
        model_applies: bool
            Indicates that the model instance has both the `relationship_attr` property and the
            `fk_attr` column required to enforce this relationship.

        """
        typ = type(target)
        return hasattr(typ, self.relationship_attr) and hasattr(typ, self.fk_attr)

    def _init_ensure_relation(self, target: M, args: Any, kwargs: Dict[str, Any]) -> None:
        """
        Called during model init to ensure that the relation is provdied.

        Checks the kwargs for the ID and the model object -- if neither is provided, provides the model
        object (this avoids an issue where the model object doesn't have a primary key yet becaue it hasn't
        been flushed to the database).

        Parameters
        ----------
        target: instance M
            Model instance targeted by the SQLAlchemy event.
        args: tuple
            Arguments passed to target's `__init__` method.
        kwargs: dict
            Keyword arguments passed to target's `__init__` method.

        Returns
        -------
        None
            Keyword arguments are modified in place if necessary.

        """
        if not self._check_instance(target):
            # Short circuit if we can't find the appropriate attributes on the instance.
            return

        try:
            if not kwargs.get(self.relationship_attr) and not kwargs.get(self.fk_attr):
                kwargs[self.relationship_attr] = self.peek()
        except NoActiveRelation:
            # TODO: Does this need to be here? Peek should never raise, but maybe defaults will raise.
            pass

    def _insert_check_relation(self, mapper: Any, connection: Any, target: M) -> None:
        if not self._check_instance(target):
            # Short circuit if we can't find the appropriate attributes on the instance.
            return

        if getattr(target, self.relationship_attr) is None and getattr(target, self.fk_attr) is None:
            if self.enforce == EnforceMode.ERROR:
                raise MissingRelation(self.basecls.__name__, self.relationship_attr, target)
            elif self.enforce == EnforceMode.WARN:
                self.logger.warning(
                    f"Missing relation {self.relationship_attr} for {self.basecls.__name__}: {target!r}"
                )
            elif self.enforce == EnforceMode.LOG:
                self.logger.debug(f"Missing relation {self.relationship_attr} for {self.basecls.__name__}: {target!r}")

    @contextlib.contextmanager
    def push(self, value: R) -> Iterator[None]:
        """
        Context manager for a particular value of the relation.

        While inside this context, the value provided will be used for the relationship property
        on any class which inherits from :attr:`basecls`. Contexts can be nested within each other,
        where the innermost context takes precedence.

        Parameters
        ----------
        value: R
            Relation value (model instance) which will be applied to every subclass of :attr:`basecls`.

        """
        self._stack.append(value)
        try:
            yield
        finally:
            # TODO: Only pop the value we pushed.
            self._stack.pop()

    @property
    def active(self) -> bool:
        """Is this context stack active and populated with a value"""
        return bool(self._stack)

    def relation(self) -> R:
        """
        Return the topmost relation value in the context stack.

        If no value is on the stack, but a default_value function is provided, the return value from that is provided
        instead. When no acceptable value can be found, :exc:`NoActiveRelation` is raised.
        """
        try:
            return self._stack[-1]
        except IndexError:
            if self.default_value is not None:
                return self.default_value()
            raise NoActiveRelation(self.basecls.__name__, self.relationship_attr)

    def peek(self) -> Optional[R]:
        """
        Return the topmost relation value in the context stack.

        If no value is on the stack, but a default_value function is provided, the return value from that is provided
        instead. When no acceptable value can be found, `None` is returned.
        """
        try:
            return self._stack[-1]
        except IndexError:
            if self.default_value is not None:
                return self.default_value()
        return None

    @property
    def proxy(self) -> LocalProxy:
        """
        Provides a proxy object which resolves to the object held by this context or the default.

        This proxies :meth:`relation` using werkzug's :class:`LocalProxy` object.
        """

        return LocalProxy(self.relation)
