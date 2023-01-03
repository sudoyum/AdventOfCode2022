#!/usr/bin/env python3

import argparse


def solve_p1(input_data):
    print(f"PART1: {0}")


def solve_p2(input_data):
    print(f"PART2: {0}")


def run_solutions(input_file, part):
    with open(input_file, "r", encoding="utf-8") as file_handle:
        input_data = file_handle.read().splitlines()

    if part == "p1":
        solve_p1(input_data)
    elif part == "p2":
        solve_p2(input_data)
    elif part == "both":
        solve_p1(input_data)
        solve_p2(input_data)

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
