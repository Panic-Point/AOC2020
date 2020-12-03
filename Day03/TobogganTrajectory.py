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
    width = len(lines[0])
    height = len(lines)
    trees = set()
    x = y = 0
    for line in lines:
        for element in line:
            if element == '#':
                trees.add((x, y))
            x = (x + 1) % width
        y += 1

    return trees, width, height


def count_trees(s: str, slope: Tuple) -> int:
    terrain = parse(s)
    trees = terrain[0]
    width = terrain[1]
    height = terrain[2]
    x = y = count = 0
    while y <= height:
        if (x, y) in trees:
            count += 1
        x = (x + slope[0]) % width
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
