#!/usr/bin/env python3

import argparse
import re
import sys
import uuid


class UnexpectedInputError(Exception):
    pass


class FileSystemNode:
    def __init__(self, name, is_directory, size=0):
        # children
        self.files = []

        self.name = name
        self.size = size
        self.is_directory = is_directory
        self.file_uuid = uuid.uuid4()
        self.dir_size = None

    def add_file(self, target_uuid, fs_node):
        if self.file_uuid == target_uuid:
            self.files.append(fs_node)
        else:
            for child in self.files:
                if child.is_directory:
                    child.add_file(target_uuid, fs_node)

    def print(self):
        if self.is_directory:
            print(f"Node: {self.name} {self.dir_size}")
        for children in self.files:
            print(f"Node: {self.name} {children.name}")
            children.print()

    def direct_child_uuid(self, name):
        for child in self.files:
            if child.is_directory and child.name == name:
                return child

    def calc_dir_size(self):
        if not self.is_directory:
            return self.size
        else:

            self.dir_size = sum([node.calc_dir_size() for node in self.files])
            return self.dir_size

    def total_dir_size(self):

        if self.is_directory:
            if self.dir_size <= 100000:
                return self.dir_size + sum(
                    [node.total_dir_size() for node in self.files]
                )

        return sum([node.total_dir_size() for node in self.files])

    def get_dirs(self, dirs):
        if self.is_directory:
            dirs.append((self.name, self.dir_size))
        for child in self.files:
            if child.is_directory:
                child.get_dirs(dirs)


def solve_p1(file_system_root):
    file_system_root.calc_dir_size()
    total_size = file_system_root.total_dir_size()
    print(f"PART1: {total_size}")


def solve_p2(file_system_root):
    dirs = []
    file_system_root.get_dirs(dirs)
    for directory in dirs:
        if directory[0] == "/":
            root_size = directory[1]

    smallest = root_size
    for directory in dirs:
        used_space = root_size - directory[1]
        if 70000000 - used_space >= 30000000:
            if directory[1] < smallest:
                smallest = directory[1]
    print(f"PART2: {smallest}")


def parse_input(input_data):
    file_system_root = FileSystemNode("/", True)

    ls_output = False

    parent_stack = [file_system_root]
    curr_node = parent_stack[-1]
    # skip first line
    for line in input_data.splitlines()[1:]:
        cmd_matches = re.search(r"\$ (ls|cd) (?:(\w+))", line)
        # line is either cd/ls command - $ or output of ls
        if line[0] == "$":
            cmd_output = False
            cmd_split = line.split(" ")
            cmd = cmd_split[1]
            if cmd == "cd":
                if cmd_split[2] == "..":
                    parent_stack.pop()
                else:
                    parent_stack.append(
                        parent_stack[-1].direct_child_uuid(cmd_split[2])
                    )
                    curr_node = parent_stack[-1]

            elif cmd == "ls":
                ls_output = True
        elif ls_output:
            dir_or_size, file_name = line.split(" ")
            if dir_or_size == "dir":
                fs_node = FileSystemNode(file_name, True)
            else:
                try:
                    size = int(dir_or_size)
                except ValueError as e:
                    raise UnexpectedInputError(
                        f"Can't convert input to size: {line}, {e}"
                    )
                fs_node = FileSystemNode(file_name, False, size=size)
            curr_node.add_file(parent_stack[-1].file_uuid, fs_node)
    return file_system_root


def run_solutions(input_file, part):
    with open(input_file, "r", encoding="utf-8") as file_handle:
        input_data = file_handle.read()

    file_system_root = parse_input(input_data)

    if part == "p1":
        solve_p1(file_system_root)
    elif part == "p2":
        solve_p2(file_system_root)
    elif part == "both":
        solve_p1(file_system_root)
        solve_p2(file_system_root)


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
