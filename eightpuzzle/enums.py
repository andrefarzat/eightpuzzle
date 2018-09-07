from enum import IntEnum

from eightpuzzle.exceptions import MovementDoesNotExistException


class Movement(IntEnum):
    up = 1
    right = 2
    down = 3
    left = 4

    @classmethod
    def get_by_name(cls, name: str) -> "Movement":
        if name == "up": return Movement.up
        if name == "right": return Movement.right
        if name == "down": return Movement.down
        if name == "left": return Movement.left
        raise MovementDoesNotExistException(name)
