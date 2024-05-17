import pytest
import os
from names import Names
from scanner import Scanner

@pytest.fixture
def scanner():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "circuit1.txt")),
        names = Names(),
        devices= Names(["CLOCK", "SWITCH", "AND", "NAND","CLK","OR", "NOR", "XOR"]),
        keywords=Names(["DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I"])
    )
@pytest.fixture
def scanner_fault():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "test_errors_circuit1.txt")),
        names = Names(),
        devices = Names(["CLOCK", "SWITCH", "AND", "NAND","CLK","OR", "NOR", "XOR"]),
        keywords = Names(["DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I"])
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

#def test_get_symbol(scanner):
#    pass
#
#def test_get_symbol_fault(scanner_fault):
#    pass



