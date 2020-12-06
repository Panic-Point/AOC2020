import time
from typing import List

start = time.time()

TEST = """abc

a
b
c

ab
ac

a
a
a
a

b"""

with open("Day06.txt", 'r') as file:
    data = file.read()


def get_groups(s: str) -> List[List]:
    result = [[]]
    groups = s.rstrip('\n').strip().split('\n\n')
    for group in groups:
        people = group.split('\n')
        result.append(people)
    if [] in result:
        result.remove([])
    return result


def get_sum(s: str) -> int:
    ans = 0
    groups = get_groups(s)
    for group in groups:
        temp_set = set()
        for element in group:
            for c in element:
                temp_set.add(c)
        ans += len(temp_set)
    return ans


assert get_sum(TEST) == 11

print(get_sum(data))


# part2
def get_sum2(s: str) -> int:
    ans = 0
    groups = get_groups(s)
    for group in groups:
        answers = set(group[0])
        if len(group) == 1:
            ans += len(answers)
        else:
            for i in range(1, len(group)):
                answers = answers.intersection(group[i])
            ans += len(answers)
    return ans


assert get_sum2(TEST) == 6

print(get_sum2(data))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))
