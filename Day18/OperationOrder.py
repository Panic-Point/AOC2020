import time

start = time.time()

TEST = """\
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

with open("Day18.txt", 'r') as file:
    data = file.read()


# http://tomerfiliba.com/blog/Infix-Operators/

class Infix:
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __or__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)


mul = Infix(lambda x, y: x * y)
add = Infix(lambda x, y: x + y)


def parse(s: str):
    lines = []
    for line in s.splitlines():
        line = line.replace('*', '|mul|')
        # remove for part 2, add for part 1
        # line = line.replace('+', '|add|')
        lines.append(line)
    return lines


INPUT = parse(data)


def solve(problems):
    ans = 0
    for p in problems:
        ans += eval(p)
    return ans


print(solve(INPUT))

print('Time taken {} seconds'.format(round(time.time() - start, 3)))
