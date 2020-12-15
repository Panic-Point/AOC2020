from time import time
from collections import defaultdict
from typing import List

start = time()

TEST = """\
0,3,6
"""

with open("Day15.txt", 'r') as file:
    data = file.read()


class Game:
    def __init__(self, numbers: List[int]):
        self.spoken = defaultdict()
        self.turn = len(numbers) + 1
        self.set_initial_spoken(numbers)

    def __repr__(self):
        return '{} {}'.format(self.turn, self.spoken)

    def say_next(self, num):
        if num in self.spoken:
            out = self.turn - self.spoken[num]
        else:
            out = 0
        self.spoken[num] = self.turn
        return out

    def set_spoken(self, num):
        self.spoken[num] = self.turn

    def set_initial_spoken(self, numbers: List[int]):
        i = 1
        for n in numbers:
            self.spoken[n] = i
            i += 1

    def play(self):
        n = 0
        while self.turn < 30000000:
            n = self.say_next(n)
            self.turn += 1
        return n


g = Game([9, 6, 0, 10, 18, 2, 1])
print(g.play())

print('Time taken {} seconds'.format(round(time() - start, 3)))
