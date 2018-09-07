from eightpuzzle import State
from eightpuzzle.enums import Movement
from eightpuzzle.exceptions import MovementDoesNotExistException, MovementNotAllowedException


class Search(object):
    current_state: State
    final_state: State

    def __init__(self, initial_state: State, final_state: State):
        self.current_state = initial_state
        self.final_state = final_state

    def do_search(self):
        raise NotImplemented()


class InteractiveSearch(Search):

    def do_search(self):
        while True:
            self.current_state.print('Current State')
            next_movement = self.get_next_move()

            try:
                self.current_state = self.current_state.move(next_movement)
            except MovementNotAllowedException:
                print("Can't move to %s" % next_movement.name)

            if self.current_state == self.final_state:
                self.current_state.print('Final state o/')
                break

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