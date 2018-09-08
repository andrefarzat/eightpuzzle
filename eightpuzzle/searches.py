from typing import List, Optional

from eightpuzzle import State
from eightpuzzle.enums import Movement
from eightpuzzle.exceptions import MovementDoesNotExistException, MovementNotAllowedException


class Search(object):
    current_state: State
    final_state: State

    def __init__(self, initial_state: State, final_state: State):
        self.current_state = initial_state
        self.final_state = final_state

    def do_search(self) -> State:
        raise NotImplemented()


class InteractiveSearch(Search):
    def do_search(self) -> State:
        while True:
            self.current_state.print('Current State')
            next_movement = self.get_next_move()

            try:
                self.current_state = self.current_state.move(next_movement)
            except MovementNotAllowedException:
                print("Can't move to %s" % next_movement.name)

            if self.current_state == self.final_state:
                return self.current_state

    def get_next_move(self) -> Movement:
        possible_movements = self.current_state.get_possible_moves()
        movement_names = [m.name for m in possible_movements]

        while True:
            print('Possible moviments: ', movement_names)
            movement_name = input('Type next movement: ')
            try:
                return Movement.get_by_name(movement_name)
            except MovementDoesNotExistException:
                print("Invalid movement: %s" % movement_name)


class DepthFirstSearch(Search):
    def do_search(self) -> State:
        return self.search_in_state(self.current_state)

    def search_in_state(self, state: State) -> State:
        # print(".", end="")
        # state.print()
        if state == self.final_state:
            return state

        next_states = [state.move(m) for m in state.get_possible_moves()]

        for next_state in next_states:
            if next_state == state.parent:
                continue

            has_found_state = self.search_in_state(next_state)
            if has_found_state:
                return has_found_state


class BreadthFirstSearch(Search):
    def do_search(self):
        states: List[State] = [self.current_state]
        
        while True:
            result = self.search_in_states(states)

            if result.found:
                return result.state
            else:
                states = result.states

    def search_in_states(self, states: List[State]) -> "SearchResult":
        next_states: List[State] = []

        for state in states:
            # print(".", end="")
            # state.print()

            result = self.search_in_state(state)
            if result.found:
                return result
            else:
                next_states.extend(result.states)

        return SearchResult(False, states=next_states)

    def search_in_state(self, state: State) -> "SearchResult":
        if state == self.final_state:
            return SearchResult(True, state=state)

        ret_states: List[State] = []
        next_states = [state.move(m) for m in state.get_possible_moves()]
        for next_state in next_states:
            if next_state == self.final_state:
                return SearchResult(True, next_state)

            if next_state != state.parent:
                ret_states.append(next_state)

        return SearchResult(False, states=ret_states)


class SearchResult(object):
    def __init__(self, found: bool, state: State = None, states: List[State] = None):
        self.found: bool = found
        self.state: Optional[State] = state
        self.states: Optional[List[State]] = states
