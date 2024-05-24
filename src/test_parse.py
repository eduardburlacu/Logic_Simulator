import pytest
import os

from names import Names
from scanner import Scanner
from parse import Parser
import os

@pytest.fixture
def scanner():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "circuit1.txt")),
        #os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "def_files", "nor.txt")),
        names = Names(),
        devices = Names(["CLOCK", "SWITCH", "AND", "NAND", "CLK","OR", "NOR", "XOR","DTYPE"]),
        keywords = Names(["DEVICES", "CONNECTIONS", "MONITORS", "DATA", "SET", "CLEAR", "Q", "QBAR","I"]),
        punct= Names([ ",", ".", ":", ";", ">", "[", "]", "=" ])
    )

@pytest.fixture
def scanner_fault():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "circuit1.txt")),
        names = Names(),
        devices = Names(["CLOCK", "SWITCH", "AND", "NAND","CLK","OR", "NOR", "XOR","DTYPE"]),
        keywords = Names(["DEVICES", "CONNECTIONS", "MONITORS", "DATA", "SET", "CLEAR", "Q", "QBAR","I"]),
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

def test_init(scanner):
    return Parser(
        names=Names(),
        devices=None,
        network=None,
        monitors=None,
        scanner=scanner,
    )

def test_parse_network(parser):

    print("\n")
    parse = parser.parse_network()
    assert parse is True

def test_parse_all():
    def claim(l:str):
        if l.upper()=="T":return True
        elif l.upper()=="F":return False
        else:
            raise RuntimeError("TEST FILE NOT PROPERLY NAMED")
    outcomes=[]
    for f in os.listdir(os.path.join(os.path.dirname(__file__),"..", "def_files")):
        #truth = claim(f[0])
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","def_files",f))
        scn = Scanner(
            path,
            names=Names(),
            devices=Names(["CLOCK", "SWITCH", "AND", "NAND", "CLK", "OR", "NOR", "XOR", "DTYPE"]),
            keywords=Names(["DEVICES", "CONNECTIONS", "MONITORS", "DATA", "SET", "CLEAR", "Q", "QBAR", "I"]),
            punct=Names([",", ".", ":", ";", ">", "[", "]", "="])
        )
        parser = Parser(
            names=Names(),
            devices=None,
            network=None,
            monitors=None,
            scanner=scn,
        )
        parse = parser.parse_network()
        #assert parse == truth
        #outcomes.append(parse)

    print(outcomes)
