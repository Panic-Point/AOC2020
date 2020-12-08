import time
from enum import Enum
from typing import List
from copy import deepcopy

start = time.time()

TEST = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

with open("Day08.txt", 'r') as file:
    data = file.read()


class Operator(Enum):
    acc = 1
    jmp = 2
    nop = 3


class Instruction(object):
    def __init__(self, op, arg, ex=None):
        if ex is None:
            self.executed = False
        else:
            self.executed = ex
        self.operation = op
        self.argument = arg

    @staticmethod
    def parse(line: str):
        op, arg = line.strip().split()
        member = Operator[op]
        ins = Instruction(member, int(arg))
        return ins

    def set_executed(self, b: bool):
        self.executed = b

    def set_operation(self, o: Operator):
        self.operation = o

    def __repr__(self):
        return "{} {} {}".format(self.operation, self.argument, self.executed)


TEST_INSTRUCTIONS = [Instruction.parse(line) for line in TEST.strip().splitlines()]
INSTRUCTIONS = [Instruction.parse(line) for line in data.strip().splitlines()]


class Computer:
    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions
        self.accumulator = 0

    def boot(self) -> int:
        temp = deepcopy(self.instructions)
        accumulator = 0
        i = 0
        while True:
            if i >= len(temp):
                break
            if temp[i].executed:
                break
            if temp[i].operation is Operator.acc:
                accumulator += temp[i].argument
                temp[i].set_executed(True)
                i += 1
            elif temp[i].operation is Operator.jmp:
                temp[i].set_executed(True)
                i += temp[i].argument
                continue
            elif temp[i].operation is Operator.nop:
                temp[i].set_executed(True)
                i += 1
                continue

        return accumulator

    def is_loop(self, instructions=None) -> bool:
        i = 0
        if instructions is None:
            instructions = self.instructions

        temp = deepcopy(instructions)

        while True:
            if i >= len(temp):
                return False
            if temp[i].executed:
                return True
            if temp[i].operation is Operator.acc:
                temp[i].set_executed(True)
                i += 1
            elif temp[i].operation is Operator.jmp:
                temp[i].set_executed(True)
                i += temp[i].argument
                continue
            elif temp[i].operation is Operator.nop:
                temp[i].set_executed(True)
                i += 1
                continue

    def fix_error(self):
        temp = deepcopy(self.instructions)
        for ins in temp:
            if ins.operation == Operator.jmp:
                ins.set_operation(Operator.nop)
                if not self.is_loop(temp):
                    return Computer(temp)
                ins.set_operation(Operator.jmp)
            elif ins.operation == Operator.nop:
                ins.set_operation(Operator.jmp)
                if not self.is_loop():
                    return Computer(temp)
                ins.set_operation(Operator.nop)
        raise RuntimeError("Could not fix error")


test_c = Computer(TEST_INSTRUCTIONS)
c = Computer(INSTRUCTIONS)
assert test_c.boot() == 5
print(c.boot())

test2 = Computer(TEST_INSTRUCTIONS)
test_fixed = test2.fix_error().boot()
c2 = Computer(INSTRUCTIONS)
c_fixed = c2.fix_error().boot()

assert test_fixed == 8
print(c_fixed)


print('Time taken {} seconds'.format(round(time.time() - start, 3)))
