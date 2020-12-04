import time
import string
from typing import Dict, List

start = time.time()

TEST = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

with open("Day04.txt", 'r') as file:
    data = file.read()

FIELDS = {'byr',
          'iyr',
          'eyr',
          'hgt',
          'hcl',
          'ecl',
          'pid',
          'cid'}


def parse(s: str) -> List[Dict]:
    out = []
    passports = s.replace('\n', ' ').split('  ')
    for p in passports:
        result = {}
        fields = p.split()
        for field in fields:
            k, v = field.split(':')
            result[k] = v
        out.append(result)

    return out


def count_valid(s: str) -> int:
    passports = parse(s)
    valid = []
    for p in passports:
        if all(field in p.keys() for field in FIELDS - {'cid'}):
            valid.append(1)
        else:
            valid.append(0)
    return sum(valid)


def count_valid2(s: str) -> int:
    passports = parse(s)
    valid = []
    for p in passports:
        if (
                all(field in p.keys() for field in FIELDS - {'cid'}) and
                1920 <= int(p['byr']) <= 2002 and
                2010 <= int(p['iyr']) <= 2020 and
                2020 <= int(p['eyr']) <= 2030 and
                p['hgt'][-2:] in {'cm', 'in'} and
                p['hcl'][0] == '#' and
                len(p['hcl']) == 7 and
                all(c in string.hexdigits for c in p['hcl'][1:]) and
                p['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'} and
                len(p['pid']) == 9 and
                p['pid'].isnumeric()
        ):
            if (p['hgt'][-2:] == 'cm' and (150 <= int(p['hgt'][:-2]) <= 193)) or \
                    (p['hgt'][-2:] == 'in' and (59 <= int(p['hgt'][:-2]) <= 76)):
                valid.append(1)
        else:
            valid.append(0)
    return sum(valid)


assert count_valid(TEST) == 2

assert count_valid(data) == 242

# part 2
INVALID = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

assert count_valid2(INVALID) == 0

VALID = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

assert count_valid2(VALID) == 4

assert count_valid2(data) == 186

print('Time taken {} seconds'.format(round(time.time() - start, 3)))
