"""Port of the Ruby gem's arguments_of_event_delegation_test.rb."""

from state_pattern import State, Stateful


class SampleState(State):
    def event(self, arg1, arg2):
        return "state event args == " + ", ".join([arg1, arg2])


class SampleStateful(Stateful):
    initial_state = SampleState


def test_arguments_pass_through():
    obj = SampleStateful()
    assert obj.event("arg1", "arg2") == "state event args == arg1, arg2"
