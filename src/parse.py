"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""
import names, devices, network, monitors, scanner

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

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.


        #----Parse Devices----
        # Check if file starts with device definitions
        current_sym = self.scanner.getsymbol()
        if current_sym.type != "DEVICES":
                self.scanner.print_line_error()
                return False
        
        #Loop though symbols provided
        while current_sym.type != "CONNECTIONS": #Read until connections 
            if current_sym.type != "NAME":
                self.scanner.print_line_error()
                return False  
            
            while current_sym != "NAME": #Read until names run out
               current_sym = self.scanner.getsymbol()
               #TODO: ADD MEMORY FUNCTION TO ASSIGN  MANY NAMES TO ONE DEVICE TYPE
               break
            
            current_sym = self.scanner.getsymbol()
            if current_sym.type != "EQUALS":
                self.scanner.print_line_error()
                return False
            
            current_sym = self.scanner.getsymbol()
            if current_sym.type != "KEYWORD": # <- TODO NEED TO IMPROVE DEVICE DETECTION
                self.scanner.print_line_error()
                return False
            
            #TODO: ADD ASSIGNMENT BUILD FUNCTION TO CREATE SPEFICIED NUMBER OF DEVICES
            current_sym = self.scanner.getsymbol() 


        #----Parse Connections----
        while current_sym.type != "MONITORS": #Read until monitors

            if current_sym.type != "NAME":
                self.scanner.print_line_error()
                return False
            
            current_sym = self.scanner.getsymbol()    
            if current_sym.type != "GREATER":
                self.scanner.print_line_error()
                return False
            
            current_sym = self.scanner.getsymbol()        
            if current_sym.type != "NAME":
                self.scanner.print_line_error()
                return False
            
            # TODO NEED TO LOOKUP DEFINED NAMES FROM DEVICES
            current_sym = self.scanner.getsymbol()
            if current_sym.type != "I":
                self.scanner.print_line_error()
                return False
            
            current_sym = self.scanner.getsymbol()
            if current_sym.type != "NUMBER":
                self.scanner.print_line_error()
                return False

            #TODO ADD CONNECTION FUNCTION TO CONNECT DEVICES
            current_sym = self.scanner.getsymbol()
            
        #----Parse Monitors----
        while current_sym.type != "EOF": #Read END
            if current_sym.type != "NAME":
                self.scanner.print_line_error()
                return False  
            
            while current_sym != "NAME": #Read until names run out
               current_sym = self.scanner.getsymbol()
               #TODO: ADD MEMORY FUNCTION TO ASSIGN  MANY NAMES TO ONE DEVICE TYPE
               break
            current_sym = self.scanner.getsymbol()

        return True
        