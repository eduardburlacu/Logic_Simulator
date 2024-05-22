import pytest
import os

from names import Names
from scanner import Scanner
from parse import Parser

@pytest.fixture
def scanner():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "circuit1.txt")),
        names = Names(),
        devices = Names(["CLOCK", "SWITCH", "AND", "NAND", "CLK","OR", "NOR", "XOR"]),
        keywords = Names(["DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I"]),
        punct= Names([ ",", ".", ":", ";", ">", "[", "]", "=" ])
    )

@pytest.fixture
def scanner_fault():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "test_errors_circuit1.txt")),
        names = Names(),
        devices = Names(["CLOCK", "SWITCH", "AND", "NAND","CLK","OR", "NOR", "XOR"]),
        keywords = Names(["DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I"]),
        punct=Names([",", ".", ":", ">", "[", "]", "="])
    )

@pytest.fixture
def parser(scanner):
    return Parser(
        names = Names(),
        devices = None,
        network = None,
        monitors = None,
        scanner = scanner,
    )

@pytest.fixture
def parser_fault(scanner_fault):
    return Parser(
        names = Names(),
        devices = None,
        network = None,
        monitors = None,
        scanner = scanner_fault,
    )

