from state_pattern.state import State, TerminalStateError


def _all_state_subclasses(cls):
    """Recursively collect all subclasses of cls."""
    result = set()
    for sub in cls.__subclasses__():
        result.add(sub)
        result.update(_all_state_subclasses(sub))
    return result


class _StatefulMeta(type):
    """Metaclass that wires up delegation from the stateful object to its
    current state instance via __getattr__."""

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        initial = namespace.get("initial_state")
        if initial is not None:
            # Collect all state methods that should be delegated.
            # Walk the MRO of the initial state to pick up methods from
            # sibling state classes referenced in transitions — but we only
            # need the initial state's declared interface because all states
            # in a family must expose the same public surface.
            cls._delegated_methods = set(initial.state_methods())


class Stateful(metaclass=_StatefulMeta):
    """Base class for objects that use the State Pattern.

    Subclass and set ``initial_state`` to a :class:`State` subclass::

        class TrafficSemaphore(Stateful):
            initial_state = Stop
    """

    initial_state: type | None = None
    _delegated_methods: set[str] = set()

    def __init__(self):
        self._current_state_instance = None

    @property
    def current_state_instance(self):
        if self._current_state_instance is None:
            self._set_state()
        return self._current_state_instance

    @property
    def state_name(self):
        """Return the class name of the current state."""
        return type(self.current_state_instance).__name__

    def restore_state(self, name):
        """Restore the machine to a state by class name.

        Skips enter/exit hooks — this is for deserialization, not a transition.
        """
        for cls in _all_state_subclasses(State):
            if cls.__name__ == name:
                self._current_state_instance = object.__new__(cls)
                self._current_state_instance.stateful = self
                self._current_state_instance.previous_state = None
                return
        raise ValueError(f"Unknown state: {name!r}")

    def _set_state(self, state_class=None):
        if state_class is None:
            state_class = self.__class__.initial_state
        if (
            self._current_state_instance is not None
            and type(self._current_state_instance) is state_class
        ):
            return self._current_state_instance
        self._current_state_instance = state_class(self, self._current_state_instance)
        return self._current_state_instance

    def transition_to(self, next_state_class):
        current = self.current_state_instance
        if current.terminal:
            raise TerminalStateError(
                f"Cannot transition from terminal state {type(current).__name__!r}"
            )
        current.exit()
        self.on_transition(current, next_state_class)
        self._set_state(next_state_class)

    def on_transition(self, from_state, to_state_class):
        """Called after exit(), before enter() on every transition.

        Override to add logging, persistence, or other cross-cutting concerns.
        ``from_state`` is the outgoing State instance, ``to_state_class`` is the
        incoming State class (not yet instantiated).
        """

    def __getattr__(self, name):
        # Only delegate methods that are declared as state methods.
        if name in self.__class__._delegated_methods:
            return getattr(self.current_state_instance, name)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )


__all__ = ["State", "Stateful", "TerminalStateError"]
