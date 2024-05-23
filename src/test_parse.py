import pytest
import os

from names import Names
from scanner import Scanner
from parse import Parser
import os

@pytest.fixture
def scanner():
    return Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "def_files", "nor.txt")),
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

def test_init(scanner):
    return Parser(
        names=Names(),
        devices=None,
        network=None,
        monitors=None,
        scanner=scanner,
    )

def test_parse_network(parser):
    check = parser.parse_network()
    assert check is True

"""
def test_decode_symbols(parser):
    answer = DEVICES KEYWORD
: PUNCT
A NAME
= PUNCT
OR DEVICE
[ PUNCT
2 NUMBER
] PUNCT
; PUNCT
B NAME
= PUNCT
NOR DEVICE
[ PUNCT
3 NUMBER
] PUNCT
; PUNCT
C NAME
= PUNCT
AND DEVICE
[ PUNCT
3 NUMBER
] PUNCT
; PUNCT
flipflop NAME
= PUNCT
DTYPE DEVICE
; PUNCT
clock NAME
= PUNCT
CLOCK DEVICE
[ PUNCT
5 NUMBER
] PUNCT
; PUNCT
input1 NAME
, PUNCT
input2 NAME
, PUNCT
set_swi NAME
, PUNCT
reset_swi NAME
= PUNCT
SWITCH DEVICE
[ PUNCT
0 NUMBER
] PUNCT
; PUNCT
input3 NAME
= PUNCT
SWITCH DEVICE
[ PUNCT
1 NUMBER
] PUNCT
; PUNCT
CONNECTIONS KEYWORD
: PUNCT
input1 NAME
> PUNCT
A NAME
. PUNCT
I1 NAME
; PUNCT
input1 NAME
> PUNCT
B NAME
. PUNCT
I1 NAME
; PUNCT
input2 NAME
> PUNCT
A NAME
. PUNCT
I2 NAME
; PUNCT
input2 NAME
> PUNCT
C NAME
. PUNCT
I2 NAME
; PUNCT
input2 NAME
> PUNCT
B NAME
. PUNCT
I2 NAME
; PUNCT
input3 NAME
> PUNCT
B NAME
. PUNCT
I3 NAME
; PUNCT
A NAME
> PUNCT
C NAME
. PUNCT
I1 NAME
; PUNCT
B NAME
> PUNCT
C NAME
. PUNCT
I3 NAME
; PUNCT
C NAME
> PUNCT
flopflip NAME
. PUNCT
DATA KEYWORD
; PUNCT
clock NAME
> PUNCT
flopflip NAME
. PUNCT
CLK DEVICE
; PUNCT
set_swi NAME
> PUNCT
flopflip NAME
. PUNCT
SET KEYWORD
; PUNCT
reset_swi NAME
> PUNCT
flopflip NAME
. PUNCT
CLEAR KEYWORD
; PUNCT
MONITORS NAME
: PUNCT
A NAME
, PUNCT
flopflip NAME
. PUNCT
Q KEYWORD
, PUNCT
flopflip NAME
. PUNCT
QBAR KEYWORD
; PUNCT
 EOF
    
    answer = answer.splitlines(keepends=False)
    print("\n")
    i=0
    while parser.symbol != None:
        assert answer[i]==f"{parser.decode()} {parser.symbol.type}"
        parser.next_symbol()
        i+=1
"""