"""Tests for terminal states."""

import pytest

from state_pattern import State, Stateful, TerminalStateError


class Active(State):
    def finish(self):
        self.transition_to(Done)

    def fail(self):
        self.transition_to(Failed)


class Done(State):
    terminal = True

    def finish(self):
        self.transition_to(Active)

    def fail(self):
        self.transition_to(Failed)


class Failed(State):
    terminal = True

    def finish(self):
        self.transition_to(Active)

    def fail(self):
        self.transition_to(Failed)


class Job(Stateful):
    initial_state = Active


def test_terminal_state_raises_on_transition():
    job = Job()
    job.finish()
    assert job.state_name == "Done"
    with pytest.raises(TerminalStateError, match="terminal state 'Done'"):
        job.finish()


def test_non_terminal_can_transition():
    job = Job()
    job.finish()
    assert job.state_name == "Done"


def test_terminal_default_is_false():
    assert Active.terminal is False


def test_terminal_set_to_true():
    assert Done.terminal is True
    assert Failed.terminal is True


def test_different_terminal_states():
    job = Job()
    job.fail()
    assert job.state_name == "Failed"
    with pytest.raises(TerminalStateError):
        job.finish()
