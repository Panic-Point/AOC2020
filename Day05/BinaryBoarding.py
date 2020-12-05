import time
import math
from typing import List

start = time.time()

TEST1 = """FBFBBFFRLR"""
TEST2 = """BFFFBBFRRR"""
TEST3 = """FFFBBBFRRR"""
TEST4 = """BBFFBBFRLL"""

NUM_ROWS = 128
NUM_COLS = 8

with open("Day05.txt", 'r') as file:
    data = file.read()


def compute_row(s: str) -> int:
    rows = list(range(NUM_ROWS))
    for c in s[:7]:
        try:
            if c == 'F':
                rows = rows[:math.floor((len(rows))/2)]
            elif c == 'B':
                rows = rows[math.ceil(len(rows)/2):]
        except ValueError:
            raise ValueError

    if len(rows) != 1:
        raise ValueError
    else:
        return rows[0]


def compute_col(s: str) -> int:
    cols = list(range(NUM_COLS))
    for c in s[-3:]:
        try:
            if c == 'L':
                cols = cols[:math.floor((len(cols))/2)]
            elif c == 'R':
                cols = cols[math.ceil(len(cols)/2):]
        except ValueError:
            raise ValueError

    if len(cols) != 1:
        raise ValueError
    else:
        return cols[0]


def compute_seat(s: str) -> int:
    r = compute_row(s)
    c = compute_col(s)
    return r * 8 + c


assert compute_seat(TEST1) == 357
assert compute_seat(TEST2) == 567
assert compute_seat(TEST3) == 119
assert compute_seat(TEST4) == 820


def find_max(s: str) -> int:
    max_id = -math.inf
    for line in s.splitlines():
        seat_id = compute_seat(line)
        if seat_id > max_id:
            max_id = seat_id
    return max_id


def find_my_seat(s: str) -> List[int]:
    ids = []
    my_seat = []
    for line in s.splitlines():
        ids.append(compute_seat(line))
    ids.sort()
    for seat in range(1, len(ids)-1):
        if ids[seat + 1] - ids[seat] != 1:
            my_seat.append(ids[seat] + 1)
    return my_seat


print(find_max(data))
print(find_my_seat(data))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))
