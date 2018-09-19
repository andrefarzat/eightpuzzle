from typing import List, Optional

from eightpuzzle import State
from eightpuzzle.enums import Movement
from eightpuzzle.exceptions import MovementDoesNotExistException, MovementNotAllowedException


FITNESS_POINT_MAP = {
    0: [4, 3, 2, 3, 2, 1, 2, 1, 0],
    1: [0, 1, 2, 1, 2, 3, 2, 3, 4],
    2: [1, 0, 1, 2, 1, 2, 3, 2, 3],
    3: [2, 1, 0, 3, 2, 1, 4, 3, 2],
    4: [1, 2, 3, 0, 1, 2, 1, 2, 3],
    5: [2, 1, 2, 1, 0, 1, 2, 1, 2],
    6: [3, 2, 1, 2, 1, 0, 3, 2, 1],
    7: [2, 3, 4, 1, 2, 3, 0, 1, 2],
    8: [3, 2, 3, 2, 1, 2, 1, 0, 1],
}


class SearchResult(object):
    def __init__(self, found: bool, state: State = None, states: List[State] = None):
        self.found: bool = found
        self.state: Optional[State] = state
        self.states: Optional[List[State]] = states


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
    def do_search(self) -> State:
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


class HillClimbingSearch(Search):
    def do_search(self) -> State:
        current: State = self.current_state
        current_fitness: int = self.evaluate(current)

        while True:
            if current == self.final_state:
                break

            neighbor, neighbor_fitness = self.get_best_of_neighborhood(self.current_state)

            if neighbor_fitness < current_fitness:
                current = neighbor
            else:
                current.print('Best local:')
                break

        return current

    @staticmethod
    def get_neighborhood(state: State) -> List[State]:
        states: List[State] = []
        for movement in state.get_possible_moves():
            neighbor = state.move(movement)

            if hasattr(state, 'parent') and neighbor == state.parent:
                continue
            states.append(neighbor)

        return states

    def get_best_of_neighborhood(self, state: State) -> (State, int):
        current: State = None
        current_fitness = 0

        for neighbor in self.get_neighborhood(state):
            neighbor_fitness = self.evaluate(neighbor)

            if current is None:
                current = neighbor
                current_fitness = neighbor_fitness
            elif neighbor_fitness < current_fitness:
                current = neighbor
                current_fitness = neighbor_fitness

        return current, current_fitness

    @staticmethod
    def evaluate(state: State) -> int:
        fitness = 0
        for i, point in enumerate(state.items):
            point_map = FITNESS_POINT_MAP[point]
            distance = point_map[i]
            fitness += distance

        return fitness


class HillClimbingWithAnnealingSearch(HillClimbingSearch):
    def do_search(self) -> State:
        while True:
            if self.current_state == self.final_state:
                break

            neighbor, _ = self.get_best_of_neighborhood(self.current_state)
            self.current_state = neighbor

        return self.current_state


class AStarSearch(Search):
    open_list: List[State] = []
    closed_list = []

    def do_search(self) -> State:
        self.open_list.append(self.current_state)

        while True:
            state = self.open_list.pop(0)
            if state == self.final_state:
                break

            states = self.get_next_states(state)
            self.open_list.extend(states)
            self.open_list.sort(key=lambda x: x.fitness)

        return state

    def get_next_states(self, state: State) -> List[State]:
        states = HillClimbingSearch.get_neighborhood(state)
        g = len(state.get_parents())

        for neighbor in states:
            neighbor.fitness = self.evaluate(neighbor) + g

        return states

    @staticmethod
    def evaluate(state: State) -> int:
        return HillClimbingSearch.evaluate(state)

