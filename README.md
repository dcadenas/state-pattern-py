# state-pattern

State Pattern for Python -- a port of the Ruby [state_pattern](https://github.com/dcadenas/state_pattern) gem.

Clean state machines with plain classes. No DSL, no decorators -- just inheritance and delegation.

## Install

```
pip install state-pattern-py
```

## Quick start

```python
from state_pattern import State, Stateful

class Stop(State):
    def next(self):
        self.transition_to(Go)
    def color(self):
        return "Red"

class Go(State):
    def next(self):
        self.transition_to(Caution)
    def color(self):
        return "Green"

class Caution(State):
    def next(self):
        self.transition_to(Stop)
    def color(self):
        return "Amber"

class TrafficSemaphore(Stateful):
    initial_state = Stop

semaphore = TrafficSemaphore()
print(semaphore.color())  # "Red"
semaphore.next()
print(semaphore.color())  # "Green"
```

Public methods defined on state classes are automatically delegated from the stateful object to its current state.

## Hooks

States can define `enter` and `exit` hooks that fire on transitions:

```python
class On(State):
    def press(self):
        self.transition_to(Off)

    def enter(self):
        print("Light is on")

    def exit(self):
        print("Light turning off")

class Off(State):
    def press(self):
        self.transition_to(On)

    def enter(self):
        print("Light is off")

class LightSwitch(Stateful):
    initial_state = Off

switch = LightSwitch()  # prints "Light is off" (enter on initial state)
switch.press()          # prints "Light turning off", then "Light is on"
```

- `enter` is called when a state is instantiated (including the initial state)
- `exit` is called before transitioning away from a state
- `enter` and `exit` are **not** delegated to the stateful object

## Accessing the context

States can reach back to the owning object through `self.stateful`:

```python
class Greeting(State):
    def greet(self):
        return f"Hello, {self.stateful.name}!"

class Greeter(Stateful):
    initial_state = Greeting

    def __init__(self, name):
        super().__init__()
        self.name = name

greeter = Greeter("World")
print(greeter.greet())  # "Hello, World!"
```

## Previous state

Each state has access to `self.previous_state`, which holds the prior state instance (or `None` for the initial state).

## Differences from the Ruby gem

| Ruby | Python |
|------|--------|
| `include StatePattern` | Inherit from `Stateful` |
| `set_initial_state Stop` | `initial_state = Stop` |
| `Forwardable` delegation | `__getattr__` delegation |
| Private methods (Ruby visibility) | Methods prefixed with `_` are not delegated |
| `stateful.method` calls the method | `self.stateful.method()` -- explicit call required |

The API philosophy is the same: states are plain classes, transitions are explicit, and conditionals are just Python -- no DSL needed.

## License

MIT
