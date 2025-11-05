import itertools
from typing import Literal


class IRobot:
    """ Represents the state of the IRobot.
    :attr board: Boolean matrix indicating whether or not a square is cleaned
    :attr on: Whether or not the robot is on
    :attr position: Current position of the robot on the board
    :attr direction: Current direction of the robot as a 2D vector
    """

    # Default row count in the board
    ROWS: int = 5
    # Default column count in the board
    COLS: int = 5
    # Mapping between the direction words and the corresponding 2D vectors
    DIRECTIONS: dict[str, tuple[int, int]] = {
        "right": (0, 1),
        "left": (0, -1),
        "up": (-1, 0),
        "down": (1, 0)
    }

    def __init__(self) -> None:
        self.board: list[list[bool]] = [[False] * self.COLS for _ in range(self.ROWS)]
        self.on: bool = False
        self.position: tuple[int, int] = (0, 0)
        self.direction: tuple[int, int] = (0, 1)

    @staticmethod
    def is_valid_direction_string(direction_str: str) -> bool:
        """ Checks if `direction_str` is a valid direction (up, down, left or right) """
        return direction_str in IRobot.DIRECTIONS

    def change_direction(self, direction: str) -> None:
        """ Changes the robot's direction to the given `direction` """
        self.direction = self.DIRECTIONS[direction]

    def strech(self) -> None:
        """ If the robot is on, cleans the adjacent squares in all directions """
        squares = itertools.product(
            (self.position[0], self.position[0] - 1, self.position[0] + 1),
            (self.position[1], self.position[1] - 1, self.position[1] + 1)
        )
        for row, col in squares:
            if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
                self.board[row][col] |= self.on

    def go(self, count: int) -> None:
        """ Advances in the current directio `count` times, and cleans each square if `self.on` is True """
        for i in range(count):
            self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            self.board[self.position[0]][self.position[1]] |= self.on

    def board_string(self) -> str:
        """ Returns a string representation of the board """
        return "\n".join("".join('X' if clean else '.' for clean in row) for row in self.board)


def main() -> None:
    robot = IRobot()
    instructions = input("Instructions: ").lower()

    for command in instructions.split():
        if command.isdigit():
            robot.go(int(command))
        elif IRobot.is_valid_direction_string(command):
            robot.change_direction(command)
        elif command in ("on", "off"):
            robot.on = command == "on"
        elif command == "strech":
            robot.strech()
        else:
            print(f"Unknown command {command}, ignoring... ")

    print(robot.board_string())


if __name__ == '__main__':
    main()
