import pytest
import os

from monitors import Monitors
from network import Network
from names import Names
from scanner import Scanner
from parse import Parser
from devices import Devices
import os


@pytest.fixture
def parser():
    pNames = Names()
    pDevices = Devices(pNames)
    pNetwork = Network(pNames, pDevices)
    pMonitors = Monitors(pNames, pDevices, pNetwork)

    scanner = Scanner(
        path=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          "..", "def_files", "nor.txt")),
        names_map=pNames,
        devices_map=Names(["CLOCK", "SWITCH", "AND", "NAND",
                           "OR", "NOR", "XOR", "DTYPE"]),
        keywords_map=Names(["DEVICES", "CONNECTIONS", "MONITORS",
                            "DATA", "CLK", "SET", "CLEAR", "Q", "QBAR", "I"]),
        punct_map=Names([",", ".", ":", ";", ">", "[", "]", "="])
    )

    return Parser(
        names=pNames,
        devices=pDevices,
        network=pNetwork,
        monitors=pMonitors,
        scanner=scanner,
    )


def test_parse_network(parser):
    parse = parser.parse_network()
    assert parse is True


def parse_all_online():
    def claim(line: str):
        if line.upper() == "T":
            return True
        elif line.upper() == "F":
            return False
        else:
            raise RuntimeError("TEST FILE NOT PROPERLY NAMED")
    outcomes = []
    for f in os.listdir(os.path.join(os.path.dirname(__file__),
                                     "..", "def_files")):
        # truth = claim(f[0])
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "..", "def_files", f))
        scn = Scanner(
            path,
            names_map=Names(),
            devices_map=Names(["CLOCK", "SWITCH", "AND", "NAND",
                               "CLK", "OR", "NOR", "XOR", "DTYPE"]),
            keywords_map=Names(["DEVICES", "CONNECTIONS", "MONITORS",
                                "DATA", "SET", "CLEAR", "Q", "QBAR", "I"]),
            punct_map=Names([",", ".", ":", ";", ">", "[", "]", "="])
        )
        pNames = Names()
        pDevices = Devices(pNames)
        pNetwork = Network(pNames, pDevices)
        pMonitors = Monitors(pNames, pDevices, pNetwork)
        parser = Parser(
            names=pNames,
            devices=pDevices,
            network=pNetwork,
            monitors=pMonitors,
            scanner=scn,
        )
        parse = parser.parse_network()
        # assert parse == truth
        outcomes.append(parse)
    print(outcomes)


def test_parse_all():
    def claim(line: str):
        if line.upper() == "T":
            return True
        elif line.upper() == "F":
            return False
        else:
            raise RuntimeError("TEST FILE NOT PROPERLY NAMED")
    outcomes = []
    for f in os.listdir(os.path.join(os.path.dirname(__file__),
                                     "..", "def_files")):
        # truth = claim(f[0])
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "..", "def_files", f))
        scn = Scanner(
            path,
            names_map=Names(),
            devices_map=Names(["CLOCK", "SWITCH", "AND", "NAND",
                               "CLK", "OR", "NOR", "XOR", "DTYPE"]),
            keywords_map=Names(["DEVICES", "CONNECTIONS", "MONITORS",
                                "DATA", "SET", "CLEAR", "Q", "QBAR", "I"]),
            punct_map=Names([",", ".", ":", ";", ">", "[", "]", "="])
        )
        pNames = Names()
        pDevices = Devices(pNames)
        pNetwork = Network(pNames, pDevices)
        pMonitors = Monitors(pNames, pDevices, pNetwork)
        parser = Parser(
            names=pNames,
            devices=pDevices,
            network=pNetwork,
            monitors=pMonitors,
            scanner=scn,
        )
        parse = parser.parse_network()
        # assert parse == truth
        outcomes.append(parse)
    print(outcomes)
    assert outcomes == [False, False, True, False, False,
                        False, False, False, False, True,
                        True, False, False, False, False,
                        False, True, False, True]


def test_skip_line(parser):
    assert parser.decode() == "DEVICES"
    for _ in range(4):
        parser.next_symbol()
    assert parser.decode() == "NOR"
    parser.next_line()
    assert parser.decode() == ";"
    for _ in range(3):
        parser.next_symbol()
    parser.next_line()
    assert parser.decode() == ";"


def test_skip_block(parser):
    assert parser.decode() == "DEVICES"
    parser.next_block()
    assert parser.decode() == "CONNECTIONS"
    for _ in range(2):
        parser.next_symbol()
    parser.next_line()
    assert parser.decode() == ";"
    parser.next_block()
    assert  parser.decode() == "MONITORS"