import time
from typing import Tuple
from collections import defaultdict

start = time.time()

TEST = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

with open("Day07.txt", 'r') as file:
    data = file.read()


def parse_line(line: str) -> Tuple:
    p1, p2 = line.split(' contain ')
    color = p1.rstrip(" bags")
    p2 = p2.rstrip('.')
    if p2 == 'no other bags':
        return color, {}

    sub_bags = p2.split(', ')
    contains = defaultdict()

    for bag in sub_bags:
        bag = bag.rstrip(' bag').rstrip(' bags')
        first_space = bag.find(" ")
        n = bag[:first_space].strip()
        sub_color = bag[first_space:].strip()
        contains[sub_color] = n
    return color, contains


def compute(s: str) -> int:
    rules = []
    for line in s.rstrip('\n').strip().splitlines():
        rules.append(parse_line(line))

    queue = ['shiny gold']
    top = set()
    while queue:
        check = queue.pop()
        for rule in rules:
            for key in rule[1]:
                if key == check:
                    queue.append(rule[0])
                    top.add(rule[0])
    return len(top)


assert compute(TEST) == 4
print(compute(data))


def bags_in_gold(s: str) -> int:
    rules = []
    for line in s.rstrip('\n').strip().splitlines():
        rules.append(parse_line(line))

    queue = ['shiny gold']
    count = 0
    while queue:
        check = queue.pop()
        for rule in rules:
            color = rule[0]
            if color == check:
                for key in rule[1]:
                    queue.extend(key for _ in range(int(rule[1][key])))
                    count += int(rule[1][key])
    return count


assert bags_in_gold(TEST) == 32
print(bags_in_gold(data))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))
