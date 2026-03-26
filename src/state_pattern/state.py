import inspect


class State:
    """Base class for all states in the State Pattern.

    Subclass this to define states. Public methods (except enter/exit and
    inherited State methods) are automatically delegated from the stateful
    object.
    """

    def __init__(self, stateful, previous_state=None):
        self.stateful = stateful
        self.previous_state = previous_state
        self.enter()

    @classmethod
    def state_methods(cls):
        """Return the set of public method names defined on this state class
        (excluding methods inherited from State itself)."""
        base_methods = set(dir(State))
        result = []
        for name in dir(cls):
            if name.startswith("_"):
                continue
            if name in base_methods:
                continue
            attr = getattr(cls, name)
            if callable(attr) and not isinstance(attr, (classmethod, staticmethod)):
                result.append(name)
        return result

    def transition_to(self, state_class):
        self.stateful.transition_to(state_class)

    def enter(self):
        pass

    def exit(self):
        pass
