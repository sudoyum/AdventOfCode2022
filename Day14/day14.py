#!/usr/bin/env python3

import argparse
import copy
import sys


class Plane:
    def __init__(self, rows=1000, cols=1000):
        self.rows = rows
        self.cols = cols
        self.plane = [["." for x in range(cols)] for y in range(rows)]

        self.lowest_x = self.lowest_y = sys.maxsize
        self.highest_x = self.highest_y = ~sys.maxsize

        self.has_floor = False

    def print_window_range(self, x_range, y_range):
        for y in range(y_range[0], y_range[1] + 1):
            for x in range(x_range[0], x_range[1] + 1):
                sys.stdout.write(self.plane[x][y])
            sys.stdout.write("\n")

    def print_window(self):
        self.print_window_range(
            (self.lowest_x - 5, self.highest_x + 5),
            (self.lowest_y - 5, self.highest_y + 5),
        )

    def process_pair(self, point_pair):
        x1, y1 = point_pair[0]
        x2, y2 = point_pair[1]

        self.lowest_x = min(x1, x2, self.lowest_x)
        self.lowest_y = min(y1, y2, self.lowest_y)

        self.highest_x = max(x1, x2, self.highest_x)
        self.highest_y = max(y1, y2, self.highest_y)

        # Only horizontal or vertical lines
        if x1 - x2 == 0:
            if y1 > y2:
                lower, upper = y2, y1
            else:
                lower, upper = y1, y2
            for i in range(lower, upper + 1):
                self.plane[x1][i] = "#"
        else:
            if x1 > x2:
                lower, upper = x2, x1
            else:
                lower, upper = x1, x2
            for i in range(lower, upper + 1):
                self.plane[i][y1] = "#"

    def sand_settling(self):
        sand_x, sand_y = (500, 0)

        if self.plane[sand_x][sand_y] == "o":
            return False

        while True:
            # P2 check for floor
            if self.has_floor:
                if sand_y == self.highest_y + 1:
                    self.plane[sand_x][sand_y] = "o"
                    return True

            if self.plane[sand_x][sand_y + 1] == ".":
                if sand_y > self.highest_y:
                    # falls into the abyss
                    return False
                sand_y += 1
                continue

            # down-left
            if self.plane[sand_x - 1][sand_y + 1] == ".":
                sand_x -= 1
                sand_y += 1
                continue

            # down-right
            if self.plane[sand_x + 1][sand_y + 1] == ".":
                sand_x += 1
                sand_y += 1
                continue

            self.plane[sand_x][sand_y] = "o"
            return True

    def insert_floor(self):
        self.has_floor = True


def solve_p1(plane):
    settled_sand = 0

    while plane.sand_settling():
        settled_sand += 1

    print(f"PART1: {settled_sand}")


def solve_p2(plane):
    settled_sand = 0

    plane.insert_floor()
    while plane.sand_settling():
        settled_sand += 1

    print(f"PART2: {settled_sand}")


def parse_input(input_data):
    plane = Plane()
    for line in input_data:
        points = []

        for coordinate in line.split("->"):
            x, y = coordinate.strip().split(",")
            points.append((int(x), int(y)))

        for i in range(len(points) - 1):
            plane.process_pair(points[i : i + 2])

    return plane


def run_solutions(input_file, part):
    with open(input_file, "r", encoding="utf-8") as file_handle:
        input_data = file_handle.read().splitlines()

    parsed_input = parse_input(input_data)

    if part == "p1":
        solve_p1(parsed_input)
    elif part == "p2":
        solve_p2(parsed_input)
    elif part == "both":
        solve_p1(copy.deepcopy(parsed_input))
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
