import pytest
import os
from names import Names
from scanner import Scanner

@pytest.fixture
def scanner():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "circuit1.txt")),
        names_map = Names(),
        devices_map = Names(["CLOCK", "SWITCH", "AND", "NAND", "CLK","OR", "NOR", "XOR"]),
        keywords_map = Names(["DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I"]),
        punct_map= Names([ ",", ".", ":", ";", ">", "[", "]", "=" ])
    )
@pytest.fixture
def scanner_fault():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "test_errors_circuit1.txt")),
        names_map = Names(),
        devices_map = Names(["CLOCK", "SWITCH", "AND", "NAND","CLK","OR", "NOR", "XOR"]),
        keywords_map = Names(["DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I"]),
        punct_map=Names([",", ".", ":", ">", "[", "]", "="])
    )

def test_get_characters(scanner):
    scanner.file.seek(0)
    assert "".join([scanner.get_next_character() for _ in range(17)]) == "DEVICES:\n    A = "
    assert scanner.current_line == 2
    assert scanner.current_line_position ==17
    assert scanner.current_character == " "

def test_skip_spaces(scanner):
    scanner.file.seek(0)
    for _ in range(9):
        scanner.get_next_character()
    scanner.skip_spaces()
    assert scanner.current_character=="A"
    assert scanner.current_line == 2
    assert scanner.current_line_position == 14
    while scanner.get_next_character()!="":
        scanner.get_next_character()
    scanner.skip_spaces()
    assert scanner.current_character==""


def test_get_name(scanner):
    scanner.file.seek(0)
    scanner.skip_spaces()
    assert scanner.get_name() == "DEVICES"


def test_skip_comment(scanner_fault):
    scanner_fault.file.seek(0)
    for _ in range(10):
        scanner_fault.get_next_character()
    sym = scanner_fault.get_symbol()
    assert sym.type=="NAME"
    assert sym.id == 0
    assert sym.line

def test_get_symbol(scanner):
    print("\n")
    scanner.file.seek(0)
    symbol = scanner.get_symbol()
    assert symbol.type == "KEYWORD"
    assert symbol.line == 1
    symbol = scanner.get_symbol()
    assert symbol.type == "PUNCT"
    assert symbol.line == 1
    symbol = scanner.get_symbol()
    assert symbol.type == "NAME"
    assert symbol.line == 2


def test_get_many_symbols(scanner):
    scanner.file.seek(0)
    print("\n")
    for _ in range(50):
        symbol = scanner.get_symbol()
        print ("SYMBOL    ",scanner.decode(symbol), symbol.id)
        #scanner.print_line_error()

def test_get_all_symbols(scanner):
    print("\n")
    symbols = scanner.get_all_symbols()

