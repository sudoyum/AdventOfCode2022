#!/usr/bin/env python3

import argparse
import logging
import re

import numpy


NUM_ROUNDS_P1 = 20
NUM_ROUNDS_P2 = 10000


def two_largest(monkies):
    largest = monkies[0].inspect_count
    second_largest = monkies[1].inspect_count
    for monkey in monkies[2:]:
        if monkey.inspect_count > largest:
            second_largest = largest
            largest = monkey.inspect_count
        elif largest > monkey.inspect_count > second_largest:
            second_largest = monkey.inspect_count
    return largest, second_largest


class Monkey:
    def __init__(self, num):
        self.num = num
        self.starting_items = []
        self.test = None
        self.if_true = None
        self.if_false = None
        self.operation = None
        self.inspect_count = 0

    def do_operation(self, old_worry):
        if self.operation[1] == "old":
            operand = old_worry
        else:
            operand = int(self.operation[1])

        match self.operation[0]:
            case "*":
                return operand * old_worry
            case "+":
                return operand + old_worry

    def turn(self, div_by_three=True, supermod=None):
        throws = []
        while len(self.starting_items) > 0:
            self.inspect_count += 1
            item = self.starting_items.pop(0)

            new_worry = self.do_operation(item)
            if div_by_three:
                new_worry = new_worry // 3
            else:
                new_worry %= supermod

            if (new_worry % self.test) == 0:
                target = self.if_true
            else:
                target = self.if_false
            throws.append((new_worry, target))
        return throws


def solve_p1(monkies):
    for i in range(NUM_ROUNDS_P1):
        for num, monkey in monkies.items():
            throws = monkey.turn()
            for throw in throws:
                monkies[throw[1]].starting_items.append(throw[0])
    largest = two_largest(list(monkies.values()))
    print(f"PART1: {largest[0] * largest[1]}")


def solve_p2(monkies):
    supermod = numpy.prod(list(set([m.test for m in list(monkies.values())])))
    for i in range(NUM_ROUNDS_P2):
        for num, monkey in monkies.items():
            throws = monkey.turn(div_by_three=False, supermod=supermod)
            for throw in throws:
                monkies[throw[1]].starting_items.append(throw[0])
    largest = two_largest(list(monkies.values()))
    print(f"PART2: {largest[0] * largest[1]}")


def parse_input(input_data):
    monkies = {}

    monkey = None
    for line in input_data.splitlines():
        monkey_match = re.match(r"Monkey (\d+)", line)
        if monkey_match:
            monkey = Monkey(int(monkey_match.group(1)))
        elif line == "":
            monkies[monkey.num] = monkey
        else:
            match line.split()[0]:
                case "Starting":
                    monkey.starting_items = [
                        int(i.strip(",")) for i in line.split()[2:]
                    ]
                case "Operation:":
                    monkey.operation = line.split()[4:]
                case "Test:":
                    monkey.test = int(line.split()[3])
                case "If":
                    if line.split()[1] == "true:":
                        monkey.if_true = int(line.split()[-1])
                    elif line.split()[1] == "false:":
                        monkey.if_false = int(line.split()[-1])
    monkies[monkey.num] = monkey
    return monkies


def run_solutions(input_file, part):
    with open(input_file, "r", encoding="utf-8") as file_handle:
        input_data = file_handle.read()

    parsed_input = parse_input(input_data)

    if part == "p1":
        solve_p1(parsed_input)
    elif part == "p2":
        solve_p2(parsed_input)
    elif part == "both":
        solve_p1(parsed_input)
        solve_p2(parsed_input)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="file containing puzzle input", type=str)
    parser.add_argument("part", help="", type=str, choices=["p1", "p2", "both"])

    args = parser.parse_args()

    try:
        run_solutions(args.input_file, args.part)
    except IOError as io_exception:
        print(f"Opening file error: {io_exception.strerror} - {args.input_file}")


if __name__ == "__main__":
    main()
