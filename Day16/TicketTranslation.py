from time import time
from collections import defaultdict

start = time()

TEST = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

TEST2 = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

with open("Day16.txt", 'r') as file:
    data = file.read()


class Ticket:
    def __init__(self, rules, my_ticket, nearby):
        self.rules = rules
        self.my_ticket = my_ticket
        self.nearby = nearby

    def __repr__(self):
        return '{} {} {}'.format(self.rules, self.my_ticket, self.nearby)

    def is_valid(self, ticket):
        all_options = set()
        for r in self.rules.values():
            all_options.update(r)

        for i in ticket:
            if int(i) not in all_options:
                return False
        return True

    def find_order(self):
        valid_nearby = []
        all_options = defaultdict()
        for ticket in self.nearby:
            if self.is_valid(ticket):
                valid_nearby.append(ticket)

        # print(valid_nearby)

        for rule in self.rules:
            options = []
            for i in range(len(self.my_ticket)):
                vals = set()
                for ticket in valid_nearby:
                    vals.add(int(ticket[i]))
                if vals.issubset(self.rules[rule]):
                    options.append(i)
            all_options[rule] = options

        while True:
            unique = [(option, all_options[option][0]) for option in all_options if len(all_options[option]) == 1]
            unique_vals = set()
            for opt, i in unique:
                unique_vals.add(i)
            # print(unique, unique_vals)
            if len(unique) == len(self.my_ticket):
                return dict(unique)

            for opt in all_options:
                if len(all_options[opt]) > 1:
                    # print(opt)
                    new_opts = [i for i in all_options[opt] if i not in unique_vals]
                    all_options[opt] = new_opts
                    # print(all_options)

    def do_it(self):
        order = self.find_order()
        # print(order)
        out = 1
        for rule in order:
            if 'departure' in rule:
                out *= int(self.my_ticket[order[rule]])
        return out


def parse(s: str):
    r2 = defaultdict()
    rules, my_ticket, others = s.rstrip().strip().split('\n\n')
    for rule in rules.splitlines():
        act_range = set()
        p1, p2 = rule.split(': ')
        ranges = p2.split(' or ')
        for r in ranges:
            begin, end = r.split('-')
            act_range.update(set(range(int(begin), int(end) + 1)))
            r2[p1] = act_range

    my_ticket = my_ticket.split('\n')[1].split(',')

    others = [ticket.split(',') for ticket in others.splitlines()[1:]]

    return r2, my_ticket, others


p = parse(data)
t = Ticket(p[0], p[1], p[2])
print(t.do_it())

print('Time taken {} seconds'.format(round(time() - start, 3)))
