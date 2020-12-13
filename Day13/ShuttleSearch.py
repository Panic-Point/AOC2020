import time
from typing import List
from functools import reduce

start = time.time()

TEST = """\
939
7,13,x,x,59,x,31,19"""
# x,x,59,x,31,19

with open("Day13.txt", 'r') as file:
    data = file.read()

TEST_BUSES = [int(i) for i in TEST.strip().splitlines()[1].split(',') if i.isnumeric()]
TEST_TIME = int(TEST.strip().splitlines()[0])
BUSES = [int(i) for i in data.strip().splitlines()[1].split(',') if i.isnumeric()]
TIME = int(data.strip().splitlines()[0])


def get_time(buses: List[int], time: int) -> int:
    times = [bus - (time % bus) for bus in buses]
    idx = times.index(min(times))
    return buses[idx] * (min(times))


print(get_time(BUSES, TIME))
print(get_time(TEST_BUSES, TEST_TIME))

NEW_BUSES = [i for i in data.strip().splitlines()[1].split(',')]
INDEXED_BUSES = [(i, int(bus)) for i, bus in enumerate(NEW_BUSES) if bus.isnumeric()]
TIMES = [(bus, (bus - i) % bus) for i, bus in INDEXED_BUSES]
N = [bus[0] for bus in TIMES]
A = [bus[1] for bus in TIMES]


# code from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


print(chinese_remainder(N, A))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))
