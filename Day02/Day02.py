from dataclasses import dataclass

import time
from collections import Counter
from typing import Tuple

start = time.time()

TEST = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

with open("Day02.txt", 'r') as file:
    data = file.read()


@dataclass
class Password:
    lo: int
    hi: int
    char: str
    password: str

    def is_valid(self) -> bool:
        counter = Counter(self.password)
        num = counter.get(self.char) or 0
        if self.lo <= num <= self.hi:
            return True
        return False

    def real_is_valid(self) -> bool:
        return (self.password[self.lo - 1] == self.char) ^ (self.password[self.hi - 1] == self.char)


def parse(s: str) -> Password:
    r, c, p = s.split()
    l, h = [int(n) for n in r.split('-')]
    c = c[0]
    return Password(l, h, c, p)


def compute(s: str) -> Tuple[int, int]:
    count = 0
    real_count = 0
    for line in s.splitlines():
        p = parse(line)
        if p.is_valid():
            count += 1
        if p.real_is_valid():
            real_count += 1
    return count, real_count


assert(compute(TEST) == (2, 1))

print(compute(data))

print('Time taken {} seconds'.format(round(time.time() - start, 2)))
