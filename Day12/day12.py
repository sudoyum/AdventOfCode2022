#!/usr/bin/env python3

import argparse
import logging
import queue
import sys


class Plane:
    D_TABLE = {(-1, 0), (1, 0), (0, -1), (0, 1)}

    def __init__(self, rows, cols):
        logging.info("rows=%d, cols=%d", rows, cols)
        self.rows = rows
        self.cols = cols
        self.plane = [[0 for x in range(cols)] for y in range(rows)]
        self.visited = None
        self.y_start = self.x_start = None
        self.y_end = self.x_end = None
        self.row_counter = 0

        self.move_count = 0
        self.nodes_left = 1
        self.nodes_in_next = 0

        self.cq = None
        self.rq = None

    def set_start(self, x, y):
        self.x_start = x
        self.y_start = y

    def reset(self, x_start, y_start):
        self.x_start = x_start
        self.y_start = y_start

        self.move_count = 0
        self.nodes_left = 1
        self.nodes_in_next = 0

    def add_row(self, row):
        for col, char in enumerate(row):
            if char == "S":
                self.y_start = self.row_counter
                self.x_start = col
                height = ord("a")
            elif char == "E":
                self.y_end = self.row_counter
                self.x_end = col
                height = ord("z")
            else:
                height = ord(row[col])

            self.plane[self.row_counter][col] = height - ord("a")
        self.row_counter += 1

    def print(self):
        for y in range(self.rows):
            for x in range(self.cols):
                sys.stdout.write(chr(self.plane[y][x] + ord("a")))
            sys.stdout.write("\n")

    def explore_neighbors(self, x_curr, y_curr):
        for dx, dy in Plane.D_TABLE:
            x_new = x_curr + dx
            y_new = y_curr + dy

            if x_new < 0 or y_new < 0:
                continue
            if x_new >= self.cols or y_new >= self.rows:
                continue

            if self.visited[y_new][x_new]:
                continue
            if self.plane[y_new][x_new] - self.plane[y_curr][x_curr] > 1:
                continue

            self.rq.put(y_new)
            self.cq.put(x_new)
            self.visited[y_new][x_new] = True
            self.nodes_in_next += 1

    # https://www.youtube.com/watch?v=KiCBXu4P-2Y
    def shortest_path(self):
        self.visited = [[False for x in range(self.cols)] for y in range(self.rows)]

        self.cq = queue.Queue()
        self.rq = queue.Queue()

        self.cq.put(self.x_start)
        self.rq.put(self.y_start)
        self.visited[self.y_start][self.x_start] = True

        found = False

        while not self.rq.empty():
            x_curr = self.cq.get()
            y_curr = self.rq.get()

            if x_curr == self.x_end and y_curr == self.y_end:
                found = True
                break

            self.explore_neighbors(x_curr, y_curr)
            self.nodes_left -= 1
            if self.nodes_left == 0:
                self.nodes_left = self.nodes_in_next
                self.nodes_in_next = 0
                self.move_count += 1

        if not found:
            return None

        return self.move_count


def solve_p1(plane):
    print(f"PART1: {plane.shortest_path()}")


def solve_p2(plane):
    curr_shortest = None

    for y in range(plane.rows):
        for x in range(plane.cols):
            if plane.plane[y][x] == 0:
                plane.reset(x, y)
                shortest_path = plane.shortest_path()
                if shortest_path is not None:
                    if curr_shortest is None or shortest_path < curr_shortest:
                        curr_shortest = shortest_path

    print(f"PART2: {curr_shortest}")


def parse_input(input_data):
    cols = len(input_data[0])
    rows = len(input_data)

    plane = Plane(rows, cols)

    for line in input_data:
        plane.add_row(line.strip("\n"))
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
        solve_p1(parsed_input)
        solve_p2(parsed_input)


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
