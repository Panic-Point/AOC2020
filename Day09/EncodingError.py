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


def parse(s: str) -> List[int]:
    numbers = s.rstrip('\n').strip().splitlines()
    return [int(x) for x in numbers]


def find_weakness(s: str, n: int) -> int:
    numbers = parse(s)
    preamble = [int(x) for x in numbers[:n]]
    numbers = numbers[n:]
    for num in numbers:
        com = combinations(preamble, 2)
        found = []
        for c in com:
            if sum(c) == num:
                found.append(num)
        if not found:
            return num
        preamble.pop(0)
        preamble.append(num)
    raise RuntimeError('No Invalid Value Found')


def find_sum(s: str, n) -> int:
    numbers = parse(s)
    check = find_weakness(s, n)
    for i in range(len(numbers)):
        l = []
        for num in numbers[i:]:
            l.append(num)
            if check == sum(l):
                return max(l) + min(l)
            if check - sum(l) > 0:
                continue
            else:
                break
    raise RuntimeError('No Sum Found')


assert find_weakness(TEST, 5) == 127
print(find_weakness(data, 25))

assert find_sum(TEST, 5) == 62
print(find_sum(data, 25))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))