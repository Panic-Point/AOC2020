import time
from typing import List

start = time.time()

TEST1 = """16
10
15
5
1
11
7
19
6
12
4"""

TEST2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

with open("Day10.txt", 'r') as file:
    data = file.read()

# class Placeholder:
#     def __int__(self):
#         pass
#
#     @staticmethod
#     def parse_line(line: str):
#         pass
#
#
# TEST_INSTRUCTIONS = [Placeholder.parse_line(line) for line in TEST.strip().splitlines()]
# INSTRUCTIONS = [Placeholder.parse(line) for line in data.strip().splitlines()]

TEST1_INPUT = [int(x) for x in TEST1.rstrip('\n').strip().splitlines()]
TEST2_INPUT = [int(x) for x in TEST2.rstrip('\n').strip().splitlines()]
INPUT = [int(x) for x in data.rstrip('\n').strip().splitlines()]


def max_chain(adapters: List[int]) -> int:
    count1 = 1
    count3 = 1
    s = sorted(adapters)
    pairs = list(zip(s, s[1:]))
    for pair in pairs:
        if max(pair) - min(pair) == 1:
            count1 += 1
        if max(pair) - min(pair) == 3:
            count3 += 1
    return count1 * count3


assert max_chain(TEST2_INPUT) == 220
print(max_chain(INPUT))

"""
Realize that any time there is a jump of 3 you must pass through that number. The indicates that a logical
way to break this down is to look at sequences between two jumps of 3
Second you have to realize that there are never any 2 jumps in the actual input. Just ones and threes, which the 
puzzle doesn't actually say that...so that is annoying.
3 3 -> 1 path
3 1 3 -> 1 path
3 1 1 3 -> 2 paths 
    0 3 4 5 8
    0 3 5 8
3 1 1 1 3 -> 4 paths 
    0 3 4 5 6 9
    0 3 4 6 9
    
    0 3 5 6 9
    
    0 3 6 9
3 1 1 1 1 3 -> 7 paths
    0 3 4 5 6 7 10
    
    0 3 4 6 7 10
    0 3 4 5 7 10
    0 3 4 7 10
    
    0 3 5 6 7 10
    0 3 5 7 10
    
    0 3 6 7 10

So count the number of one jumps between two 3 jumps and the pattern ends up being the tribonacci sequence
https://brilliant.org/wiki/tribonacci-sequence/. 

We can find all of these sequences and multiply the number of chains together for the answer
"""


def number_of_chains(adapters: List[int]) -> int:
    s = sorted(adapters)

    # add in initial 0 to make it work
    s.insert(0, 0)
    prev = s[0]
    one_jumps = 1
    count = 1

    for n in s[1:]:
        if n == prev + 1:
            one_jumps += 1
        elif one_jumps > 1:
            count *= tribonacci(one_jumps)
            one_jumps = 1
        prev = n

    # end with streak of one jumps
    if one_jumps > 1:
        count *= tribonacci(one_jumps)

    return count


def tribonacci(n: int, memo=None) -> int:
    if memo is None:
        memo = {0: 0, 1: 1, 2: 1}
    if n not in memo:
        memo[n] = tribonacci(n - 1, memo) + tribonacci(n - 2, memo) + tribonacci(n - 3, memo)
    return memo[n]


"""Very similar to above. This works without knowing the tribonacci sequence.
1. Create a 0 array of required lenght
2. Fill in array as you go
3. Paths to get to n is just the sum of the way to get to the 3 previous numbers
4. Add base cases
5. compute
"""


def number_of_chains2(adapters: List[int]) -> int:
    s = sorted(adapters)

    max_check = max(s) + 3
    s.append(max_check)

    memo = [0] * (max_check + 1)

    memo[0] = 1

    if 1 in adapters:
        memo[1] = 1

    if 1 in adapters and 2 in adapters:
        memo[2] = 2
    elif 2 in adapters:
        memo[2] = 1

    for n in range(3, max_check + 1):
        if n not in s:
            continue
        memo[n] = memo[n - 1] + memo[n - 2] + memo[n - 3]
    return memo[max_check]


assert number_of_chains(TEST2_INPUT) == 19208
assert number_of_chains2(TEST2_INPUT) == 19208
print(number_of_chains(INPUT))
print('Time taken {} seconds'.format(round(time.time() - start, 3)))
