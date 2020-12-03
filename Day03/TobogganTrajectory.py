import time
from typing import Tuple, Set

start = time.time()

TEST = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

with open("Day03.txt", 'r') as file:
    data = file.read()

SLOPES = [(1, 1),
          (3, 1),
          (5, 1),
          (7, 1),
          (1, 2)]


def parse(s: str) -> Tuple[Set, int, int]:
    lines = s.splitlines()
    max_x = len(lines[0])
    max_y = len(lines)
    trees = set()
    x = y = 0
    for line in lines:
        for element in line:
            if element == '#':
                trees.add((x, y))
            x = (x + 1) % max_x
        y += 1

    return trees, max_x, max_y


def count_trees(s: str, slope: Tuple) -> int:
    puzzle_map = parse(s)
    trees = puzzle_map[0]
    length = puzzle_map[1]
    distance = puzzle_map[2]
    x = y = count = 0
    while y <= distance:
        if (x, y) in trees:
            count += 1
        x = (x + slope[0]) % length
        y += slope[1]
    return count


assert count_trees(TEST, (3, 1)) == 7

# part 1
assert count_trees(data, (3, 1)) == 151


def all_slopes(s: str) -> int:
    result = 1
    for slope in SLOPES:
        result *= count_trees(s, slope)
    return result


assert all_slopes(TEST) == 336

# part 2
assert all_slopes(data) == 7540141059


print('Time taken {} seconds'.format(round(time.time() - start, 2)))
