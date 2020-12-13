import time
from typing import List, Tuple
from enum import Enum
from copy import deepcopy
import numpy as np

start = time.time()

TEST = """\
F10
N3
F7
R90
F11"""

with open("Day12.txt", 'r') as file:
    data = file.read()


class Direction(Enum):
    E = 0
    N = 90
    W = 180
    S = 270


class Instruction:
    def __init__(self, action, value):
        self.action = action
        self.value = value

    def __repr__(self):
        return "{}, {}".format(self.action, self.value)

    @staticmethod
    def parse_line(line: str):
        action = line[0]
        value = int(line[1:])
        return Instruction(action, value)

    def step(self, coor: List, direction: Direction) -> Tuple:
        # North is Positive Y
        if self.action == 'N':
            coor[1] += self.value
        # South is Negative Y
        if self.action == 'S':
            coor[1] -= self.value
        # East is Positive X
        if self.action == 'E':
            coor[0] += self.value
        # West is Negative X
        if self.action == 'W':
            coor[0] -= self.value
        # left is positive on unit circle
        if self.action == 'L':
            new_direction = Direction((direction.value + self.value) % 360)
            direction = new_direction
        # right is negative on unit circle
        if self.action == 'R':
            new_direction = Direction((direction.value - self.value) % 360)
            direction = new_direction
        if self.action == 'F':
            self.action = str(direction.name)
            return self.step(coor, direction)
        return coor, direction

    def waypoint_step(self, coor: List, waypoint: List) -> Tuple:
        # North is Positive Y
        if self.action == 'N':
            waypoint[1] += self.value
        # South is Negative Y
        if self.action == 'S':
            waypoint[1] -= self.value
        # East is Positive X
        if self.action == 'E':
            waypoint[0] += self.value
        # West is Negative X
        if self.action == 'W':
            waypoint[0] -= self.value
        if self.action in 'L':
            cos, sin = np.cos(np.radians(self.value)), np.sin(np.radians(self.value))
            new_waypoint = np.dot(np.array([[cos, -sin], [sin, cos]]), [waypoint[0], waypoint[1]])
            waypoint[0] = new_waypoint[0]
            waypoint[1] = new_waypoint[1]
        if self.action in 'R':
            cos, sin = np.cos(np.radians(self.value)), np.sin(np.radians(self.value))
            m = np.array([[cos, sin], [-sin, cos]])
            new_waypoint = np.dot(m, [waypoint[0], waypoint[1]])
            waypoint[0] = new_waypoint[0]
            waypoint[1] = new_waypoint[1]

        if self.action == 'F':
            coor[0] += waypoint[0]*self.value
            coor[1] += waypoint[1]*self.value
        return coor, waypoint


TEST_INSTRUCTIONS = [Instruction.parse_line(line) for line in TEST.splitlines()]
INSTRUCTIONS = [Instruction.parse_line(line) for line in data.splitlines()]


def compute(instructions: List[Instruction]):
    coor = [0, 0]
    direction = Direction.E

    for ins in instructions:
        coor, direction = ins.step(coor, direction)

    return abs(coor[0]) + abs(coor[1])


def compute2(instructions: List[Instruction]):
    coor = [0, 0]
    waypoint = [10, 1]

    for ins in instructions:
        coor, waypoint = ins.waypoint_step(coor, waypoint)

    return abs(coor[0]) + abs(coor[1])


# print(compute2(TEST_INSTRUCTIONS))
print(compute(deepcopy(INSTRUCTIONS)))
print(round(compute2(deepcopy(INSTRUCTIONS)), 0))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))
