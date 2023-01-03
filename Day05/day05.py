#!/usr/bin/env python3

import argparse
import re
import sys


class UnexpectedInputError(Exception):
    pass


class Boxes:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.boxes = [[" " for x in range(rows)] for y in range(cols)]
        self.stacks = []

    def stack(self):
        for j in range(self.rows):
            column = []

            for i in range(self.cols - 1, -1, -1):
                if self.boxes[i][j] != " ":
                    column.append(self.boxes[i][j])

            self.stacks.append(column)

    def print(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.boxes[i][j] == " ":
                    sys.stdout.write(self.boxes[i][j] * 4)
                else:
                    sys.stdout.write(self.boxes[i][j] + " ")
            sys.stdout.write("\n")

    def print_stacks(self):
        for stack in self.stacks:
            if len(stack) > 0:
                sys.stdout.write(stack[-1].strip("]["))
        sys.stdout.write("\n")

    def top_boxes(self):
        top_boxes = ""
        for stack in self.stacks:
            if len(stack) > 0:
                top_boxes += stack[-1].strip("][")
        return top_boxes

    def move(self, move):
        mv_num, mv_src, mv_dest = move

        for _ in range(mv_num):
            top = self.stacks[mv_src - 1].pop()
            self.stacks[mv_dest - 1].append(top)

    def move9001(self, move):
        mv_num, mv_src, mv_dest = move

        top = self.stacks[mv_src - 1][-mv_num:]
        self.stacks[mv_dest - 1] += top
        self.stacks[mv_src - 1] = self.stacks[mv_src - 1][:-(mv_num)]


def solve_p1(parsed_input):
    boxes, moves = parsed_input
    boxes.stack()
    for move in moves:
        boxes.move(move)

    top_boxes = boxes.top_boxes()
    print(f"PART1: {top_boxes}")


def solve_p2(parsed_input):
    boxes, moves = parsed_input
    boxes.stack()
    for move in moves:
        boxes.move9001(move)

    top_boxes = boxes.top_boxes()
    print(f"PART2: {top_boxes}")


def parse_input(input_data):
    boxes = Boxes(9, 8)

    input_iter = iter(input_data.splitlines())

    for index, line in enumerate(input_iter):
        if index < boxes.cols:
            box_line = line.split(" ")

            count = 0
            cleaned_boxes = []
            for i in box_line:
                if i == "":
                    count += 1
                else:
                    cleaned_boxes.append(i)
                if count == 4:
                    cleaned_boxes.append(" ")
                    count = 0
            boxes.boxes[index] = cleaned_boxes
        else:
            if line == "":
                break

    # move instructions
    moves = []
    for line in input_iter:
        regex_match = re.search(r"move (\d+) from (\d+) to (\d+)", line)
        if regex_match:
            mv_num, mv_src, mv_dest = regex_match.groups()
            moves.append((int(mv_num), int(mv_src), int(mv_dest)))
        else:
            raise UnexpectedInputError(f"Issue with regex for input {line}")

    return (boxes, moves)


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
