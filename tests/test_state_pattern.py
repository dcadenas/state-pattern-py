"""Port of the Ruby gem's state_pattern_test.rb."""

from state_pattern import State, Stateful


# -- Family fixture (mirrors Ruby's Family module) --


class James(State):
    def name(self):
        self.transition_to(Lynn)
        return f"James {self.stateful.last_name()}"

    def james_method(self):
        pass


class Lynn(State):
    def name(self):
        self.transition_to(James)
        return f"Lynn {self.stateful.last_name()}"

    def james_method(self):
        pass


class Member(Stateful):
    initial_state = Lynn

    def last_name(self):
        return "Holbrook"


# -- Button fixture --


class Off(State):
    def press(self):
        self.transition_to(On)


class On(State):
    def press(self):
        self.transition_to(Off)


class Button(Stateful):
    initial_state = Off


# -- Tests --


def test_initial_state_name():
    member = Member()
    assert member.name() == "Lynn Holbrook"


def test_transition_cycles():
    member = Member()
    assert member.name() == "Lynn Holbrook"
    assert member.name() == "James Holbrook"
    assert member.name() == "Lynn Holbrook"


def test_all_state_methods_available():
    """All public methods from the state are delegated, even if they belong to
    another state in the family."""
    member = Member()
    assert hasattr(member, "james_method")


def test_button_toggle():
    button = Button()
    assert isinstance(button.current_state_instance, Off)
    button.press()
    assert isinstance(button.current_state_instance, On)
    button.press()
    assert isinstance(button.current_state_instance, Off)


def test_independent_instances():
    b1 = Button()
    b2 = Button()
    b1.press()
    assert isinstance(b1.current_state_instance, On)
    assert isinstance(b2.current_state_instance, Off)


def test_multiple_stateful_classes():
    member = Member()
    button = Button()
    member.name()
    button.press()
    assert isinstance(member.current_state_instance, James)
    assert isinstance(button.current_state_instance, On)
