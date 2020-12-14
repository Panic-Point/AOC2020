from time import time
from collections import defaultdict
import itertools
import re

start = time()

TEST = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

TEST2 = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

with open("Day14.txt", 'r') as file:
    data = file.read()


class Computer:
    def __init__(self, mask=None):
        self.mask = mask
        self.memory = defaultdict()
        self.addresses = defaultdict()
        self.mem_val = 0

    def __repr__(self):
        return '{} {} {} {}'.format(self.mask, self.memory, self.addresses, self.mem_val)

    # Part 1
    # def write_memory(self, mem, add):
    #     result = [add[i] if self.mask[i] == 'X' else self.mask[i] for i in range(len(add))]
    #     result = ''.join(result)
    #     self.memory[mem] = result

    # Part 2
    def write_memory(self, mem, add):
        for val in self.addresses[mem]:
            self.set_memory(int(val, 2), add)

    def decode_memory(self, val):
        addresses = []
        result = [val[i] if self.mask[i] == '0' else '1' if self.mask[i] == '1' else 'X' for i in range(len(val))]
        idxs = [i for i in range(len(result)) if result[i] == 'X']
        options = [['0', '1'] for _ in idxs]
        for choice in itertools.product(*options):
            subs = iter(choice)
            temp = result[:]
            for i in range(len(temp)):
                if temp[i] == 'X':
                    temp[i] = next(subs)
            addresses.append(''.join(temp))
        self.set_addresses(int(val, 2), addresses)

    def set_mask(self, mask):
        self.mask = mask

    def set_memory(self, key, value):
        self.memory[key] = value

    def set_addresses(self, key, value):
        self.addresses[key] = value

    def add_mem_val(self, val):
        self.mem_val += val

    def initialize(self, s: str):
        for line in s.splitlines():
            if line.split(' = ')[0] == 'mask':
                self.set_mask(line.split(' = ')[1])
            else:
                p1, v = line.split(' = ')
                v = bin(int(v))[2:]
                while len(v) < 36:
                    v = v.rjust(len(v)+1, '0')
                m, = re.search(r"\[(\w+)]", p1).groups()
                bin_m = bin(int(m))[2:]
                while len(bin_m) < 36:
                    bin_m = bin_m.rjust(len(bin_m)+1, '0')
                self.decode_memory(bin_m)
                self.write_memory(int(m), v)

        for key in self.memory:
            self.add_mem_val(int(self.memory[key], 2))
        return self.mem_val


c = Computer()

print(c.initialize(data))

print('Time taken {} seconds'.format(round(time() - start, 3)))
