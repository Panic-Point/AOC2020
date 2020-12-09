import time
from typing import List
from itertools import combinations


start = time.time()

TEST = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

with open("Day09.txt", 'r') as file:
    data = file.read()


TEST_INPUT = [int(x) for x in TEST.rstrip('\n').strip().splitlines()]
INPUT = [int(x) for x in data.rstrip('\n').strip().splitlines()]


def find_weakness(numbers: List[int], n: int) -> int:
    preamble = [int(x) for x in numbers[:n]]
    numbers = numbers[n:]
    for num in numbers:
        sums = {sum(c) for c in combinations(preamble, 2)}
        if num not in sums:
            return num
        preamble.pop(0)
        preamble.append(num)
    raise RuntimeError('No Invalid Value Found')


def find_sum(numbers: List[int], n) -> int:
    check = find_weakness(numbers, n)
    for i in range(len(numbers)):
        possibility = []
        for num in numbers[i:]:
            possibility.append(num)
            if check == sum(possibility):
                return max(possibility) + min(possibility)
            if check - sum(possibility) > 0:
                continue
            else:
                break
    raise RuntimeError('No Sum Found')


assert find_weakness(TEST_INPUT, 5) == 127
print(find_weakness(INPUT, 25))

assert find_sum(TEST_INPUT, 5) == 62
print(find_sum(INPUT, 25))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))