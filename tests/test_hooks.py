"""Port of the Ruby gem's hook_test.rb."""

from state_pattern import State, Stateful


class HookOn(State):
    def press(self):
        self.transition_to(HookOff)
        self.stateful.messages.append(f"{self.stateful.button_name()} is off")

    def enter(self):
        self.stateful.messages.append("Entered the On state")

    def exit(self):
        self.stateful.messages.append("Exited the On state")

    def _private_method(self):
        pass


class HookOff(State):
    def press(self):
        self.transition_to(HookOn)
        self.stateful.messages.append(f"{self.stateful.button_name()} is on")

    def enter(self):
        self.stateful.messages.append("Entered the Off state")

    def exit(self):
        self.stateful.messages.append("Exited the Off state")


class HookButton(Stateful):
    initial_state = HookOff

    def __init__(self):
        super().__init__()
        self.messages: list[str] = []

    def button_name(self):
        return "Button"


def test_hooks_after_one_press():
    button = HookButton()
    button.press()
    assert button.messages == [
        "Entered the Off state",
        "Exited the Off state",
        "Entered the On state",
        "Button is on",
    ]


def test_hooks_after_two_presses():
    button = HookButton()
    button.press()
    button.press()
    assert button.messages == [
        "Entered the Off state",
        "Exited the Off state",
        "Entered the On state",
        "Button is on",
        "Exited the On state",
        "Entered the Off state",
        "Button is off",
    ]


def test_enter_exit_not_delegated():
    button = HookButton()
    assert "enter" not in HookButton._delegated_methods
    assert "exit" not in HookButton._delegated_methods


def test_private_method_not_delegated():
    button = HookButton()
    assert not hasattr(button, "_private_method")


def test_press_is_delegated():
    button = HookButton()
    assert hasattr(button, "press")
