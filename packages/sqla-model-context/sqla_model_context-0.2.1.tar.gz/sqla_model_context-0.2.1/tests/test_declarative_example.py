import pytest
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.event import contains
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from sqla_model_context import ModelRelativeContextManager
from sqla_model_context.context import MissingRelation

Base = declarative_base()


class Manager(Base):
    __tablename__ = "manager"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    manager_id = Column(Integer, ForeignKey("manager.id"))
    manager = relationship(Manager)


@pytest.fixture
def engine():
    uri = "sqlite:///:memory:"
    engine = create_engine(uri)

    yield engine

    engine.dispose()


@pytest.fixture
def session(engine):
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    yield Session()

    Base.metadata.drop_all(engine)


@pytest.fixture
def ctx():
    c = ModelRelativeContextManager(Employee, "manager", listen=False)
    with c.listen() as ct:
        yield ct


def test_add_listeners(session, ctx):

    assert contains(Employee, "init", ctx._init_ensure_relation)
    assert contains(Employee, "before_insert", ctx._insert_check_relation)


def test_empty_manager(session, ctx):
    e = Employee(name="Bernard")

    assert e.manager is None
    assert e.manager_id is None


def test_provided_manager(session, ctx):
    m = Manager(name="Cato")
    e = Employee(name="Bernard", manager=m)

    assert e.manager == m


def test_context_manager(session, ctx):
    s = Manager(name="Darren")
    m = Manager(name="Cato")

    with ctx.push(s):
        e = Employee(name="Bernard", manager=m)

    assert e.manager == m

    with ctx.push(s):
        e2 = Employee(name="Edward")

    assert e2.manager == s


def test_insert_present(session, ctx):

    s = Manager(name="Darren")
    session.add(s)
    with ctx.push(s):
        e = Employee(name="Edward")
    session.add(e)

    session.commit()

    e2 = session.query(Employee).filter(Employee.name == "Edward").one()
    assert e2.manager.name == "Darren"


def test_insert_missing(session, ctx):

    s = Manager(name="Darren")
    session.add(s)
    e = Employee(name="Edward")
    session.add(e)

    with pytest.raises(MissingRelation):
        session.commit()


def test_insert_no_enforcement(session):
    ctx = ModelRelativeContextManager(Employee, "manager", enforce=False, listen=False)

    assert ctx.enforce.name == "NONE"

    with ctx.listen():
        assert not contains(Employee, "before_insert", ctx._insert_check_relation)

        s = Manager(name="Darren")
        session.add(s)
        e = Employee(name="Edward")
        session.add(e)

        session.commit()


def test_multi_listener_attachment(session):
    ctx = ModelRelativeContextManager(Employee, "manager", enforce=False, listen=True)

    with pytest.warns(Warning):
        with ctx.listen():
            pass
