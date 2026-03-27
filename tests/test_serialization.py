"""Tests for state_name and restore_state serialization support."""

import pytest

from state_pattern import State, Stateful


class Idle(State):
    def work(self):
        self.transition_to(Running)


class Running(State):
    def work(self):
        self.transition_to(Idle)


class Machine(Stateful):
    initial_state = Idle


def test_state_name_returns_class_name():
    m = Machine()
    assert m.state_name == "Idle"
    m.work()
    assert m.state_name == "Running"


def test_restore_state_sets_current_state():
    m = Machine()
    m.restore_state("Running")
    assert m.state_name == "Running"
    assert isinstance(m.current_state_instance, Running)


def test_restore_state_skips_hooks():
    messages = []

    class TrackedA(State):
        def go(self):
            self.transition_to(TrackedB)

        def enter(self):
            messages.append("enter A")

    class TrackedB(State):
        def go(self):
            self.transition_to(TrackedA)

        def enter(self):
            messages.append("enter B")

    class Tracked(Stateful):
        initial_state = TrackedA

    t = Tracked()
    _ = t.state_name  # trigger lazy init of initial state
    assert messages == ["enter A"]
    messages.clear()

    t.restore_state("TrackedB")
    assert messages == []
    assert t.state_name == "TrackedB"


def test_restore_state_unknown_name_raises():
    m = Machine()
    with pytest.raises(ValueError, match="Unknown state: 'Nonexistent'"):
        m.restore_state("Nonexistent")


def test_restore_roundtrip():
    m1 = Machine()
    m1.work()
    name = m1.state_name

    m2 = Machine()
    m2.restore_state(name)
    assert m2.state_name == m1.state_name
