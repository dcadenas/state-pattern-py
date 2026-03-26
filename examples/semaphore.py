"""Traffic semaphore example — direct port of the Ruby gem's example."""

import time

from state_pattern import State, Stateful


class Stop(State):
    def next(self):
        time.sleep(3)
        self.transition_to(Go)

    def color(self):
        return "Red"


class Go(State):
    def next(self):
        time.sleep(2)
        self.transition_to(Caution)

    def color(self):
        return "Green"


class Caution(State):
    def next(self):
        time.sleep(1)
        self.transition_to(Stop)

    def color(self):
        return "Amber"


class TrafficSemaphore(Stateful):
    initial_state = Stop


if __name__ == "__main__":
    semaphore = TrafficSemaphore()
    while True:
        print(semaphore.color())
        semaphore.next()
