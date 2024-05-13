"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""
import os
import names, devices, network, monitors, scanner

#Find ebnf grammar definitions
ebnf_path = os.path.join(os.path.dirname(__file__),"..","doc","EBNF","ebnf.txt")
#print(ebnf_path) #Uncomment for debugging
ebnf_file = open(ebnf_path, 'r')


class Parser:
    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names, devices, network, monitors, scanner):
        """Initialise constants."""
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner
        self.grammar = ebnf_file

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        #Analyse EBNF Grammar
        ebnf_string = self.grammar.read().replace("\n","")
        ebnf_list = ebnf_string.split(" ;") #Split into each rule of the grammmar

        #Split each rule into RHS and LHS
        for i in range(len(ebnf_list)):
            ebnf_list[i] = ebnf_list[i].replace(" ","")          
            ebnf_list[i] = ebnf_list[i].split("=")

        
        return True
        