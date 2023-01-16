#!/usr/bin/env python3

import argparse
import logging
import re


class UnexpectedInputError(Exception):
    pass


def need_update_tail(tail_pos, head_pos):
    return (abs(tail_pos[1] - head_pos[1]) > 1) or (abs(tail_pos[0] - head_pos[0]) > 1)


class SnakePlane:
    DTABLE = {"L": (-1, 0), "R": (1, 0), "U": (0, -1), "D": (0, 1)}

    def __init__(self, num_elements):
        self.num_elements = num_elements
        self.elements = [(0, 0) for _ in range(num_elements)]

        self.visited = set()
        self.visited.add(self.elements[-1])

        self.rows, self.cols = None, None
        self.plane = None

    def _setup_plane(self):
        pass

    def print(self):
        if self.plane is None:
            self._setup_plane()

        for i in range(self.cols):
            for j in range(self.rows):
                sys.stdout.write(str(self.trees[i][j]))
            sys.stdout.write("\n")

    def update_tail(self, tail_pos, head_pos):
        # vertical or horizontal
        dx = head_pos[0] - tail_pos[0]
        dy = head_pos[1] - tail_pos[1]

        if dy == 0:
            if head_pos[0] > tail_pos[0]:
                # right
                return (tail_pos[0] + 1, tail_pos[1])
            else:
                # left
                return (tail_pos[0] - 1, tail_pos[1])
        elif dx == 0:
            if head_pos[1] > tail_pos[1]:
                # up
                return (tail_pos[0], tail_pos[1] + 1)
            else:
                # down
                return (tail_pos[0], tail_pos[1] - 1)
        # diagonal
        else:
            if dy > 0 and dx > 0:
                return (tail_pos[0] + 1, tail_pos[1] + 1)
            elif dx > 0 and dy < 0:
                return (tail_pos[0] + 1, tail_pos[1] - 1)
            elif dx < 0 and dy > 0:
                return (tail_pos[0] - 1, tail_pos[1] + 1)
            elif dx < 0 and dy < 0:
                return (tail_pos[0] - 1, tail_pos[1] - 1)
            else:
                raise ValueError("dx=%d, dy=%d", dx, dy)

    def update(self, direction):
        dx, dy = SnakePlane.DTABLE[direction]

        self.elements[0] = (self.elements[0][0] + dx, self.elements[0][1] + dy)

        for i in range(self.num_elements - 1):
            if need_update_tail(self.elements[i + 1], self.elements[i]):
                self.elements[i + 1] = self.update_tail(
                    self.elements[i + 1], self.elements[i]
                )
                self.visited.add(self.elements[-1])


def update_tail(tail_pos, head_pos):
    # vertical or horizontal
    dx = head_pos[0] - tail_pos[0]
    dy = head_pos[1] - tail_pos[1]

    if dy == 0:
        if head_pos[0] > tail_pos[0]:
            # right
            return (tail_pos[0] + 1, tail_pos[1])
        else:
            # left
            return (tail_pos[0] - 1, tail_pos[1])
    elif dx == 0:
        if head_pos[1] > tail_pos[1]:
            # up
            return (tail_pos[0], tail_pos[1] + 1)
        else:
            # down
            return (tail_pos[0], tail_pos[1] - 1)
    # diagonal
    else:
        if dy > 0 and dx > 0:
            return (tail_pos[0] + 1, tail_pos[1] + 1)
        elif dx > 0 and dy < 0:
            return (tail_pos[0] + 1, tail_pos[1] - 1)
        elif dx < 0 and dy > 0:
            return (tail_pos[0] - 1, tail_pos[1] + 1)
        elif dx < 0 and dy < 0:
            return (tail_pos[0] - 1, tail_pos[1] - 1)
        else:
            raise ValueError("dx=%d, dy=%d", dx, dy)


def solve_p1(input_data):
    tail_pos, head_pos = (0, 0), (0, 0)

    visited = set()
    visited.add(tail_pos)

    for line in input_data:
        instruction = re.match(r"(U|D|R|L) (\d+)", line)
        if instruction:
            dx, dy = SnakePlane.DTABLE[instruction.group(1)]
            for i in range(int(instruction.group(2))):
                head_pos = (head_pos[0] + dx, head_pos[1] + dy)
                if need_update_tail(tail_pos, head_pos):
                    tail_pos = update_tail(tail_pos, head_pos)
                    visited.add(tail_pos)
        else:
            raise UnexpectedInputError(f"Issue with regex for input {line}")

    print(f"PART1: {len(visited)}")


def solve_p2(input_data):
    snake_plane = SnakePlane(10)
    for line in input_data:
        instruction = re.match(r"(U|D|R|L) (\d+)", line)
        if instruction:
            direction = instruction.group(1)
            for i in range(int(instruction.group(2))):
                snake_plane.update(direction)
    print(f"PART2: {len(snake_plane.visited)}")


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
    except UnexpectedInputError as uie_exception:
        print(f"Input data not in expected format: {uie_exception}, exiting")


if __name__ == "__main__":
    main()
