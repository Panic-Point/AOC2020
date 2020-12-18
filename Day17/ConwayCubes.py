from time import time
from typing import NamedTuple, Set

start = time()

TEST = """\
.#.
..#
###"""

ADJACENT_SEATS = set()

with open("Day17.txt", 'r') as file:
    data = file.read()


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int
    w: int

    def get_neighbors(self):
        neighbors = set()
        for dx, dy, dz, dw in ADJACENT_SEATS:
            if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                neighbors.add(Coordinate(self.x - dx, self.y - dy, self.z - dz, self.w - dw))
        return neighbors


for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            for w in range(-1, 2):
                ADJACENT_SEATS.add(Coordinate(x, y, z, w))


class Cube:
    def __init__(self, active: Set[Coordinate]):
        self.active = active
        self.inactive_candidates = self.get_candidates()

    def __repr__(self):
        return '{}'.format([point for point in self.active])

    def __len__(self):
        return len(self.active)

    def get_candidates(self):
        cand = set()
        for point in self.active:
            for coor in point.get_neighbors():
                if coor not in self.active:
                    cand.add(coor)
        return cand

    def set_active(self, active):
        self.active = active

    def set_inactive(self, inactive):
        self.inactive_candidates = inactive

    def count_active_neighbors(self, c: Coordinate):
        count = 0
        for point in c.get_neighbors():
            if point in self.active:
                count += 1
        return count

    def update(self):
        active = self.active.copy()
        inactive = self.inactive_candidates.copy()
        for i in self.active:
            if self.count_active_neighbors(i) not in {2, 3}:
                active.remove(i)
        for j in self.inactive_candidates:
            if self.count_active_neighbors(j) == 3:
                active.add(j)
                inactive.remove(j)
        self.set_active(active)
        self.set_inactive(self.get_candidates())

    def boot(self):
        for i in range(6):
            self.update()
        return self


def parse(s: str):
    lines = s.split('\n')
    return Cube({Coordinate(x, y, 0, 0) for x, row in enumerate(lines) for y, c in enumerate(row) if c == '#'})


TEST_GRID = parse(TEST)
print(TEST_GRID)
TEST_GRID.boot()
print(len(TEST_GRID))

INPUT = parse(data)
INPUT.boot()
print(len(INPUT))

print('Time taken {} seconds'.format(round(time() - start, 3)))
