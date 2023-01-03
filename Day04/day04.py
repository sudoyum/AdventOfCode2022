#!/usr/bin/env python3

import argparse
import re


class UnexpectedInputError(Exception):
    pass


def solve_p1(parsed_input):
    num_overlapping = 0
    # low1, upper1, low2, upper2
    for item in parsed_input:
        if item[0] <= item[2] and item[1] >= item[3] or\
           item[2] <= item[0] and item[3] >= item[1]:
            num_overlapping += 1
    print(f"PART1: {num_overlapping}")


def solve_p2(parsed_input):
    not_overlapping = 0
    for item in parsed_input:
        if item[0] < item[2] and item[1] < item[2] or\
           item[0] > item[3] and item[1] > item[3]:
            not_overlapping += 1
    print(f"PART2: {len(parsed_input) - not_overlapping}")


def parse_input(input_data):
    parsed_input = []

    for line in input_data.splitlines():
        regex_matches = re.search(r"(\d+)-(\d+),(\d+)-(\d+)", line)
        if regex_matches:
            low1, upper1, low2, upper2 = regex_matches.groups()
            parsed_input.append((int(low1), int(upper1), int(low2), int(upper2)))
        else:
            raise UnexpectedInputError(f"Issue with regex for input {line}")
    return parsed_input


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
    except UnexpectedInputError as uie_exception:
        print(f"Input data not in expected format: {uie_exception}, exiting")


if __name__ == "__main__":
    main()
