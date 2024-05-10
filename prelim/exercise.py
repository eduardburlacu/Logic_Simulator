#!/usr/bin/env python3
"""Preliminary exercises for Part IIA Project GF2."""
import sys
import os
# Insert main project directory so that we can resolve the src imports
src_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, src_path)
from mynames import MyNames

def open_file(path):
    """Open and return the file specified by path."""
    try:
        file = open(path, "r")
    except IOError as e:
        raise e
    return file


def get_next_character(input_file):
    """Read and return the next character in input_file."""
    char = input_file.read(1)
    # Enable if you want to get rid of linespaces
    # if char == "\n":
    #    char = input_file.read(1)
    return char


def get_next_non_whitespace_character(input_file):
    """Seek and return the next non-whitespace character in input_file."""
    while True:
        ch = get_next_character(input_file)
        if ch != " " or ch == "":
            return ch


def get_next_number(input_file):
    """Seek the next number in input_file.
    Return the number (or None) and the next non-numeric character.
    """
    ch = get_next_character(input_file)
    number = ""
    while ch != "":
        while ch.isdigit():
            number = number + ch
            ch = get_next_character(input_file)
        if number != "":
            break
        else:
            ch = get_next_character(input_file)
    return [number, ch]


def get_next_name(input_file):
    """Seek the next name string in input_file.

    Return the name string (or None) and the next non-alphanumeric character.
    """
    ch = get_next_character(input_file)
    while not ch.isalpha():
        ch = get_next_character(input_file)
        if ch == "":
            return [None, ch]
    name = ""
    while ch != "":
        while ch.isalnum():
            name = name + ch
            ch = get_next_character(input_file)
        if name != "":
            break
        else:
            ch = get_next_character(input_file)
    if name == "":
        name = None
    return [name, ch]


def main():
    """Preliminary exercises for Part IIA Project GF2."""

    # Check command line arguments
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Error! One command line argument is required.")
        sys.exit()

    else:
        print("\nNow opening file...")
        # Print the path provided and try to open the file for reading
        print(arguments[0])
        file = open_file(arguments[0])
        print("\nNow reading file...")
        # Print out all the characters in the file, until the end of file
        ch = get_next_character(file)
        while ch != "":
            print(ch, end="")
            ch = get_next_character(file)

        file.seek(0)
        print("\nNow skipping spaces...")
        # Print out all the characters in the file, without spaces
        ch = get_next_non_whitespace_character(file)
        while ch != "":
            print(ch, end="")
            ch = get_next_non_whitespace_character(file)

        file.seek(0)
        print("\nNow reading numbers...")
        # Print out all the numbers in the file
        while True:
            number, next_ch = get_next_number(file)
            print(number, end=" ")
            if next_ch == "":
                break
        file.seek(0)
        print("\nNow reading names...")
        # Print out all the names in the file
        while True:
            name, next_ch = get_next_name(file)
            if name is not None:
                print(name, end=" ")
            if next_ch == "":
                break

        file.seek(0)
        print("\nNow censoring bad names...")
        # Print out only the good names in the file
        name_table = MyNames()
        bad_name_ids = [
            name_table.lookup("Terrible"),
            name_table.lookup("Horrid"),
            name_table.lookup("Ghastly"),
            name_table.lookup("Awful")
        ]
        while True:
            name, next_ch = get_next_name(file)
            if name is not None:
                if name_table.lookup(name) not in bad_name_ids:
                    print(name, end=" ")
            if next_ch == "":
                break


if __name__ == "__main__":
    main()
