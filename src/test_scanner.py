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

def test_get_characters(scanner):
    assert "".join([scanner.get_next_character() for _ in range(17)]) == "DEVICES:\n    A = "
