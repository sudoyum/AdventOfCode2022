#!/usr/bin/env python3

import argparse
import queue

D_TABLE = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def cube_neighbors(cube):
    neighbors = []
    for dx, dy, dz in D_TABLE:
        neighbors.append((cube[0] + dx, cube[1] + dy, cube[2] + dz))
    return neighbors


def solve_p1(cubes):
    exposed_sides = 0
    for cube in cubes:
        for neighbor in cube_neighbors(cube):
            if neighbor not in cubes:
                exposed_sides += 1
    print(f"PART1: {exposed_sides}")


def space(cube, min_cube, max_cube):
    return all(min_cube[i] <= cube[i] <= max_cube[i] for i in range(3))


def solve_p2(cubes):
    # bfs
    exposed_sides = 0
    cube_q = queue.Queue()
    visited = set()

    min_cube = [min(cube[i] - 1 for cube in cubes) for i in range(3)]
    max_cube = [max(cube[i] + 1 for cube in cubes) for i in range(3)]
    print(min_cube)
    print(max_cube)

    cube_q.put(max_cube)

    while not cube_q.empty():
        curr_cube = cube_q.get()
        if curr_cube in cubes:
            exposed_sides += 1
        elif tuple(curr_cube) not in visited:
            visited.add(tuple(curr_cube))
            for neighbor in cube_neighbors(curr_cube):
                if space(neighbor, min_cube, max_cube):
                    cube_q.put(neighbor)
    print(f"PART2: {exposed_sides}")


def run_solutions(input_file, part):
    with open(input_file, "r", encoding="utf-8") as file_handle:
        input_data = file_handle.read().splitlines()

    cubes = [tuple(int(i) for i in line.split(",")) for line in input_data]

    if part == "p1":
        solve_p1(cubes)
    elif part == "p2":
        solve_p2(cubes)
    elif part == "both":
        solve_p1(cubes)
        solve_p2(cubes)


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
