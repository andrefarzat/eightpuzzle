from typing import List

from eightpuzzle.enums import Movement
from eightpuzzle.exceptions import MovementNotAllowedException


class State(object):
    default_items_position: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    items: List[int]
    possible_moves: List[Movement]

    def __init__(self, *items: int):
        self.items = list(items) if items is not None else State.default_items_position

    def get_possible_moves(self) -> List[Movement]:
        if self.possible_moves:
            return self.possible_moves

        zero_position = self.items.index(0)
        moves = []

        if zero_position in (3, 4, 5, 6, 7, 8):
            moves.append(Movement.up)

        if zero_position in (0, 1, 3, 4, 6, 7):
            moves.append(Movement.right)

        if zero_position in (0, 1, 2, 3, 4, 5):
            moves.append(Movement.down)

        if zero_position in (1, 2, 4, 5, 7, 8):
            moves.append(Movement.left)

        self.possible_moves = moves
        return moves

    def is_move_possible(self, movement: Movement) -> bool:
        return movement in self.get_possible_moves()

    def move(self, movement: Movement) -> "State":
        if not self.is_move_possible(movement):
            raise MovementNotAllowedException()

        items = self.items.copy()
        zero_position = items.index(0)

        if movement == Movement.up:
            next_position = zero_position - 3
        elif movement == Movement.right:
            next_position = zero_position + 1
        elif movement == Movement.down:
            next_position = zero_position + 3
        elif movement == Movement.left:
            next_position = zero_position - 1
        else:
            raise MovementNotAllowedException()

        items[zero_position], items[next_position] = items[next_position], items[zero_position]
        return State(items)
