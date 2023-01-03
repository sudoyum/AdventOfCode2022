#!/usr/bin/env python3

import argparse
import re
import sys


class UnexpectedInputError(Exception):
    pass


class Instruction:
    def __init__(self, inst, amnt):
        self.inst = inst
        self.amnt = None
        if inst == "addx":
            self.amnt = int(amnt.strip())


class Screen:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.screen = [[0 for x in range(rows)] for y in range(cols)]

    def print(self):
        for i in range(self.cols):
            for j in range(self.rows):
                char = "#" if self.screen[i][j] == 1 else "."
                sys.stdout.write(str(char))
            sys.stdout.write("\n")

    def draw_screen(self, cycle, x_register):
        if x_register in (cycle % 40, cycle % 40 - 1, cycle % 40 + 1):
            self.screen[int(cycle / 40)][(cycle % 40)] = 1


def solve(parsed_input):
    signal_strength, inst_index = 0, 0
    x_register, cycle = 1, 1
    cycle_waiting = False

    instruction = None

    rows = 40
    cols = 6
    screen = Screen(rows, cols)

    while len(parsed_input) > inst_index or cycle_waiting:
        if not cycle_waiting:
            instruction = parsed_input[inst_index]
            if instruction.inst == "addx":
                cycle_waiting = True
            inst_index += 1
        else:
            x_register += instruction.amnt
            cycle_waiting = False

        screen.draw_screen(cycle, x_register)

        cycle += 1

        if cycle in [20, 60, 100, 140, 180, 220]:
            signal_strength += cycle * x_register
    print(f"PART1: {signal_strength}")
    print("PART2:")
    screen.print()


def parse_input(input_data):
    parsed_input = []

    for line in input_data.splitlines():
        regex_matches = re.search(r"(noop|addx)(?:([-0-9\s]+))?", line)
        if regex_matches:
            inst, amnt = regex_matches.groups()
            parsed_input.append(Instruction(inst, amnt))
        else:
            raise UnexpectedInputError(f"Issue with regex for input {line}")
    return parsed_input


def run_solutions(input_file, part):
    with open(input_file, "r", encoding="utf-8") as file_handle:
        input_data = file_handle.read()

    parsed_input = parse_input(input_data)
    solve(parsed_input)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="file containing puzzle input", type=str)
    parser.add_argument("part", help="", type=str, choices=["p1", "p2", "both"])

    args = parser.parse_args()

    try:
        run_solutions(args.input_file, args.part)
    except IOError as io_exception:
        print(f"Opening file error: {io_exception.strerror} - {args.input_file}")
    except UnexpectedInputError as uie_exception:
        print(f"Input data not in expected format: {uie_exception}, exiting")


if __name__ == "__main__":
    main()
