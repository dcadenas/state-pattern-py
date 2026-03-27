"""Tests for the on_transition hook on Stateful."""

from state_pattern import State, Stateful


class Off(State):
    def press(self):
        self.transition_to(On)


class On(State):
    def press(self):
        self.transition_to(Off)


class LoggingSwitch(Stateful):
    initial_state = Off

    def __init__(self):
        super().__init__()
        self.log: list[tuple[str, str]] = []

    def on_transition(self, from_state, to_state_class):
        self.log.append((type(from_state).__name__, to_state_class.__name__))


def test_on_transition_called():
    switch = LoggingSwitch()
    switch.press()
    assert switch.log == [("Off", "On")]


def test_on_transition_called_on_every_transition():
    switch = LoggingSwitch()
    switch.press()
    switch.press()
    switch.press()
    assert switch.log == [("Off", "On"), ("On", "Off"), ("Off", "On")]


def test_on_transition_receives_outgoing_instance():
    captured = []

    class A(State):
        def go(self):
            self.transition_to(B)

    class B(State):
        def go(self):
            self.transition_to(A)

    class Inspector(Stateful):
        initial_state = A

        def __init__(self):
            super().__init__()

        def on_transition(self, from_state, to_state_class):
            captured.append(from_state)

    obj = Inspector()
    obj.go()
    assert isinstance(captured[0], A)
    assert captured[0].stateful is obj


def test_default_on_transition_is_noop():
    class SimpleSwitch(Stateful):
        initial_state = Off

    switch = SimpleSwitch()
    switch.press()
    assert isinstance(switch.current_state_instance, On)
