from typing import Generic
from typing import TypeVar

M = TypeVar("M")
#: The target model

__all__ = [
    "ContextRelationWarning",
    "ContextRelationListenerWarning",
    "ContextRelationError",
    "MissingRelation",
    "NoActiveRelation",
]


class ContextRelationWarning(Warning):
    pass


class ContextRelationListenerWarning(ContextRelationWarning):
    """Warning raised when listeners are added twice"""


class ContextRelationError(Exception):
    """Error class encompasing potential problems with the context relation manager"""


class MissingRelation(ContextRelationError, Generic[M]):
    """Error indicating that a model is being saved without an appropriate value for a relationship"""

    def __init__(self, clsname: str, relationship_name: str, target: M) -> None:
        super().__init__()
        self.clsname = clsname
        self.relationship_name = relationship_name
        self.target = target

    def __str__(self) -> str:
        return f"Missing relation {self.relationship_name} for {self.clsname}: {self.target!r}"


class NoActiveRelation(ContextRelationError):
    """Error indicating that no relationship is currently active in the relationship context manager"""

    def __init__(self, clsname: str, relationship_name: str):
        self.clsname = clsname
        self.relationship_name = relationship_name

    def __str__(self) -> str:
        return f"No currently active relation {self.relationship_name} for {self.clsname} - context was empty"
