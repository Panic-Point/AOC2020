# https://adventofcode.com/2020/day/1

from itertools import combinations
import time
start = time.time()
TEST = """1721
979
366
299
675
1456"""

with open("Day01.txt", 'r') as file:
    data = file.read()


def compute(s: str) -> int:
    numbers = set([int(n) for n in s.split() if int(n) < 2020])
    for n in numbers:
        if 2020 - n in numbers:
            return n * (2020 - n)


assert (compute(TEST) == 514579)

print(compute(data))


def compute3(s: str) -> int:
    numbers = set([int(n) for n in s.split() if int(n) < 2020])
    com = combinations(numbers, 3)
    for c in com:
        if sum(c) == 2020:
            return c[0] * c[1] * c[2]


assert (compute3(TEST) == 241861950)

print(compute3(data))
print('Time taken {} seconds'.format(round(time.time() - start, 2)))
