import time
from typing import List
from collections import Counter
from copy import deepcopy

start = time.time()

TEST = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

with open("Day11.txt", 'r') as file:
    data = file.read()

Grid = List[List[str]]
TEST_GRID = [list(row) for row in TEST.split('\n')]
INPUT_GRID = [list(row) for row in data.strip().rstrip().split('\n')]
ADJACENT_SEATS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 1), (-1, 1), (1, 0), (1, 1)]


def count_neighbors(grid: Grid, i: int, j: int) -> int:
    count = Counter(grid[i + x][j + y]
                    for x, y in ADJACENT_SEATS
                    if 0 <= i + x < len(grid) and 0 <= j + y < len(grid[0]))
    return count['#']


def count_seen(grid: Grid, i: int, j: int) -> int:
    num_rows = len(grid)
    num_cols = len(grid[0])

    seen = []

    for x, y in ADJACENT_SEATS:
        seat = '.'
        di = i
        dj = j
        while seat not in 'L#&':
            di += x
            dj += y

            if 0 <= di < num_rows and 0 <= dj < num_cols:
                seat = grid[di][dj]
            else:
                seat = '&'
        seen.append(seat)

    count = Counter(seen)
    return count['#']


def seat_change(grid: Grid, i: int, j: int) -> str:
    seat = grid[i][j]
    if seat == 'L' and count_neighbors(grid, i, j) == 0:
        new_state = '#'
    elif seat == '#' and count_neighbors(grid, i, j) >= 4:
        new_state = 'L'
    else:
        new_state = seat
    return new_state


def seat_change2(grid: Grid, i: int, j: int) -> str:
    seat = grid[i][j]
    if seat == 'L' and count_seen(grid, i, j) == 0:
        new_state = '#'
    elif seat == '#' and count_seen(grid, i, j) >= 5:
        new_state = 'L'
    else:
        new_state = seat
    return new_state


def change_state(grid: Grid) -> Grid:
    new_grid = deepcopy(grid)
    for i in range(len(new_grid)):
        for j in range(len(new_grid[i])):
            # change for part1 or part 2
            new_grid[i][j] = seat_change(grid, i, j)
    return new_grid


def stabilize(grid: Grid) -> int:
    # Assume rectangle
    num_rows = len(grid)
    num_cols = len(grid[0])
    new_grid = change_state(grid)
    if new_grid == grid:
        count = Counter(new_grid[i][j] for i in range(num_rows) for j in range(num_cols))
        return count['#']
    else:
        return stabilize(new_grid)


# print(stabilize(TEST_GRID))
print(stabilize(INPUT_GRID))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))
