#!/usr/bin/env python3

import argparse
import logging
import sys


class Plane:
    def __init__(self, rows, cols):
        logging.info("rows=%d, cols=%d", rows, cols)
        self.rows = rows
        self.cols = cols
        self.trees = [[0 for x in range(rows)] for y in range(cols)]
        self.col_counter = 0
        self.highest_scenic_score = -1
        self.d_table = {"L": (-1, 0), "R": (1, 0), "U": (0, -1), "D": (0, 1)}

    def add_row(self, row):
        for j in range(self.rows):
            self.trees[self.col_counter][j] = int(row[j])
        self.col_counter += 1

    def print(self):
        for i in range(self.cols):
            for j in range(self.rows):
                sys.stdout.write(str(self.trees[i][j]))
            sys.stdout.write("\n")

    def _is_visible(self, i, j, direction):
        dx, dy = self.d_table[direction]
        curr_dx, curr_dy = dx, dy

        while self._inbounds(i + curr_dy, j + curr_dx):
            if self.trees[i + curr_dy][j + curr_dx] >= self.trees[i][j]:
                return False
            curr_dx += dx
            curr_dy += dy
        return True

    def is_visible(self, i, j):
        return (
            self._is_visible(i, j, "L")
            or self._is_visible(i, j, "R")
            or self._is_visible(i, j, "U")
            or self._is_visible(i, j, "D")
        )

    def _inbounds(self, i, j):
        return (i >= 0 and i < self.rows) and (j >= 0 and j < self.cols)

    def _calc_scenic_score(self, i, j, direction):
        ss = 0
        dx, dy = self.d_table[direction]
        curr_dx, curr_dy = dx, dy

        while self._inbounds(i + curr_dy, j + curr_dx):
            ss += 1
            if self.trees[i + curr_dy][j + curr_dx] >= self.trees[i][j]:
                break
            curr_dx += dx
            curr_dy += dy
        return ss

    def calc_scenic_score(self, i, j):
        ss_up, ss_down, ss_left, ss_right = 0, 0, 0, 0

        ss_up = self._calc_scenic_score(i, j, "U")
        ss_down = self._calc_scenic_score(i, j, "D")
        ss_left = self._calc_scenic_score(i, j, "L")
        ss_right = self._calc_scenic_score(i, j, "R")

        scenic_score = ss_up * ss_down * ss_left * ss_right
        if scenic_score > self.highest_scenic_score:
            self.highest_scenic_score = scenic_score


def solve_p1(plane):

    visible = 0
    for i in range(plane.rows):
        for j in range(plane.cols):
            # edges
            if i == 0 or j == 0 or i == plane.rows - 1 or j == plane.cols - 1:
                visible += 1
            else:
                if plane.is_visible(i, j):
                    visible += 1

    print(f"PART1: {visible}")


def solve_p2(plane):
    for i in range(plane.rows):
        for j in range(plane.cols):
            plane.calc_scenic_score(i, j)
    print(f"PART2: {plane.highest_scenic_score}")


def parse_data(input_data):
    cols = len(input_data[0])
    rows = len(input_data)
    plane = Plane(rows, cols)
    for line in input_data:
        plane.add_row(line)
    return plane


def run_solutions(input_file, part):
    with open(input_file, "r", encoding="utf-8") as file_handle:
        input_data = file_handle.read().splitlines()

    parsed_data = parse_data(input_data)

    if part == "p1":
        solve_p1(parsed_data)
    elif part == "p2":
        solve_p2(parsed_data)
    elif part == "both":
        solve_p1(parsed_data)
        solve_p2(parsed_data)


def main():
    logging.basicConfig(
        format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
        level=logging.ERROR,
    )

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
