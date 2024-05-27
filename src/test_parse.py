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
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "def_files", "dtype.txt")),
        #os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "def_files", "nor.txt")),
        names_map = pNames,
        devices_map = Names(["CLOCK", "SWITCH", "AND", "NAND","OR", "NOR", "XOR","DTYPE"]),
        keywords_map = Names(["DEVICES", "CONNECTIONS", "MONITORS", "DATA", "CLK", "SET", "CLEAR", "Q", "QBAR","I"]),
        punct_map = Names([ ",", ".", ":", ";", ">", "[", "]", "=" ])
    )

    return Parser(
        names = pNames,
        devices = pDevices,
        network = pNetwork,
        monitors = pMonitors,
        scanner = scanner,
    )



def test_parse_network(parser):

    #print("\n")
    parse = parser.parse_network()
    #print(parser.names.names_list)
    #print(parser.connections_defined)
    #print(f"XOR TRUE ID IS {parser.devices.XOR}")

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
            names_map=Names(),
            devices_map=Names(["CLOCK", "SWITCH", "AND", "NAND", "CLK", "OR", "NOR", "XOR", "DTYPE"]),
            keywords_map=Names(["DEVICES", "CONNECTIONS", "MONITORS", "DATA", "SET", "CLEAR", "Q", "QBAR", "I"]),
            punct_map=Names([",", ".", ":", ";", ">", "[", "]", "="])
        )
        pNames = Names()
        pDevices = Devices(pNames)
        pNetwork = Network(pNames, pDevices)
        pMonitors = Monitors(pNames, pDevices, pNetwork)
        parser = Parser(
            names=pNames,
            devices = pDevices,
            network = pNetwork,
            monitors = pMonitors,
            scanner=scn,
        )
        parse = parser.parse_network()
        #assert parse == truth
        outcomes.append(parse)

    print(outcomes)
