#!/usr/bin/env python
"""Tests for `sqla_model_context` package."""
import logging
from typing import NamedTuple
from typing import Optional

import pytest

from sqla_model_context import EnforceMode
from sqla_model_context import ModelRelativeContextManager
from sqla_model_context.context import MissingRelation
from sqla_model_context.context import NoActiveRelation


class Model(NamedTuple):
    relation: Optional["Relation"]
    relation_id: Optional[str]


class Relation(NamedTuple):
    id: str


def new(name: str) -> Model:
    return Model(Relation(name), f"{name}-id")


@pytest.mark.parametrize(
    "input, expected",
    [
        (True, EnforceMode.ERROR),
        (False, EnforceMode.NONE),
        ("WARN", EnforceMode.WARN),
        (EnforceMode.LOG, EnforceMode.LOG),
    ],
)
def test_enforce_mode(input, expected):

    assert EnforceMode.parse_arg(input) == expected


@pytest.fixture
def ctx():
    return ModelRelativeContextManager(basecls=Model, relationship_attr="relation", listen=False)


def test_context_manager_basic(ctx):

    assert ctx.fk_attr == "relation_id"
    assert repr(ctx).startswith("ModelRelativeContextManager(")


def test_context_manager_check_instance(ctx):

    assert ctx._check_instance(Model("foo", "foo-id"))
    assert not ctx._check_instance("foo")


class TestInitEnsureRelation:
    def test_simple_empty(self, ctx):
        mkw = dict(relation="foo", relation_id="foo-id")
        m = Model(**mkw)

        # Should move on successfully.
        ctx._init_ensure_relation(m, (), mkw)
        assert m.relation == "foo"

    def test_simple_pushed(self, ctx):
        mkw = dict(relation="foo", relation_id="foo-id")
        m = Model(**mkw)
        r = Relation(id="bar-id")

        with ctx.push(r):
            ctx._init_ensure_relation(m, (), mkw)
            assert ctx.active

        assert not ctx.active
        assert mkw["relation"] == "foo"

    def test_short_circuit(self, ctx):
        ctx._init_ensure_relation("bah", (), {})

    def test_pushed_missing(self, ctx):
        mkw = dict(relation="foo", relation_id="foo-id")
        m = Model(**mkw)
        r = Relation(id="bar-id")

        mkw = {}
        with ctx.push(r):
            ctx._init_ensure_relation(m, (), mkw)
            assert ctx.active
        assert mkw["relation"] == r

    def test_init_missing(self, ctx):
        mkw = dict(relation="foo", relation_id="foo-id")
        m = Model(**mkw)
        # r = Relation(id="bar-id")

        mkw = {}
        ctx._init_ensure_relation(m, (), mkw)


class TestCheckInsert:
    def test_short_circuit(self, ctx, caplog):
        ctx._insert_check_relation(None, None, "bah")

        assert not caplog.records

    def test_present(self, ctx, caplog):
        mkw = dict(relation="foo", relation_id="foo-id")
        m = Model(**mkw)
        ctx._insert_check_relation(None, None, m)

    def test_missing(self, ctx):
        m = Model(None, None)
        with pytest.raises(MissingRelation):
            ctx._insert_check_relation(None, None, m)

    def test_missing_warn(self, ctx, caplog):
        m = Model(None, None)
        ctx.enforce = EnforceMode.WARN

        ctx._insert_check_relation(None, None, m)
        assert caplog.records

        assert caplog.records[0].levelno == logging.WARNING

    def test_missing_log(self, ctx, caplog):
        m = Model(None, None)
        ctx.enforce = EnforceMode.LOG

        ctx._insert_check_relation(None, None, m)
        assert caplog.records

        assert caplog.records[0].levelno == logging.DEBUG

    def test_missing_nothing(self, ctx, caplog):
        m = Model(None, None)
        ctx.enforce = EnforceMode.NONE

        ctx._insert_check_relation(None, None, m)
        assert not caplog.records


class TestProxy:
    def test_present(self, ctx):
        proxy = ctx.proxy
        with ctx.push(new("foo")):
            assert proxy.relation.id == "foo"

            with ctx.push(new("bar")):
                assert proxy.relation.id == "bar"

    def test_missing(self, ctx):
        proxy = ctx.proxy

        with pytest.raises(NoActiveRelation):
            proxy.relation.id
