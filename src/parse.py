"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""

from names import Names
from scanner import Scanner, Symbol
from devices import Devices
from monitors import Monitors
from network import Network
import logging
from typing import Union, Dict

class ErrorHandler:
    def __init__(self):
        self.error_code_map:Dict = {}
        self.error_count: int = 0
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

    @property
    def get_error_count(self)->int:
        return self.error_count

    def register_error(self, error_code:int, error_msg):
        if not isinstance(error_code, int):
            raise ValueError("Error code must be an integer")
        self.error_code_map[error_code] = error_msg

    def log_error(self, error_code:int, *args,**kwargs):
        """
        Handles an error by logging it.
        Args:
            error_code (int): The error code to log.
            *args: Additional arguments to be logged with the error message.
            **kwargs: Additional keyword arguments to be logged with the error message.
        """
        if error_code not in self.error_code_map:
            self.logger.error(f"Unknown error code: {error_code}")

        error_message = self.error_code_map[error_code].format(*args, **kwargs)
        self.logger.error(error_message)
        self.error_count += 1


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
        self.names: Names = names
        self.devices: Devices = devices
        self.network: Network = network
        self.monitors: Monitors = monitors
        self.scanner: Scanner = scanner

        self.error_handler= ErrorHandler()
        self.symbol:Union[Symbol,None] = None


    def parse_devices(self)->bool:
        # ----Parse Devices----

        if self.symbol.type != self.scanner.KEYWORD and self.scanner.devices_map.get_name_string( self.symbol.id) != "DEVICES":
            # TODO: RAISE EXCEPTION FOR WRONG SYNTAX
            return False


        """        
        # Loop though symbols provided
        while self.symbol.type != "CONNECTIONS":  # Read until connections
            if self.symbol.type != "NAME":
                self.scanner.print_line_error()
                return False

            while self.symbol != "NAME":  # Read until names run out
                self.symbol = self.scanner.get_symbol()
                # TODO: ADD MEMORY FUNCTION TO ASSIGN  MANY NAMES TO ONE DEVICE TYPE
                break

            self.symbol = self.scanner.get_symbol()
            if self.symbol.type != "EQUALS":
                self.scanner.print_line_error()
                return False

            self.symbol = self.scanner.get_symbol()
            if self.symbol.type != "KEYWORD":  # <- TODO NEED TO IMPROVE DEVICE DETECTION
                self.scanner.print_line_error()
                return False

            # TODO: ADD ASSIGNMENT BUILD FUNCTION TO CREATE SPEFICIED NUMBER OF DEVICES
            self.symbol = self.scanner.get_symbol()
            """


    def parse_connections(self)->bool:
        # ----Parse Connections----
        while self.symbol.type != "MONITORS":  # Read until monitors

            if self.symbol.type != "NAME":
                self.scanner.print_line_error()
                return False

            self.symbol = self.scanner.get_symbol()
            if self.symbol.type != "GREATER":
                self.scanner.print_line_error()
                return False

            self.symbol = self.scanner.get_symbol()
            if self.symbol.type != "NAME":
                self.scanner.print_line_error()
                return False

            # TODO NEED TO LOOKUP DEFINED NAMES FROM DEVICES
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type != "I":
                self.scanner.print_line_error()
                return False

            self.symbol = self.scanner.get_symbol()
            if self.symbol.type != "NUMBER":
                self.scanner.print_line_error()
                return False

            # TODO ADD CONNECTION FUNCTION TO CONNECT DEVICES
            self.symbol = self.scanner.get_symbol()


    def parse_monitors(self)->bool:
        # ----Parse Monitors----
        while self.symbol.type != "EOF":  # Read END
            if self.symbol.type != "NAME":
                self.scanner.print_line_error()
                return False

            while self.symbol != "NAME":  # Read until names run out
                self.symbol = self.scanner.get_symbol()
                # TODO: ADD MEMORY FUNCTION TO ASSIGN  MANY NAMES TO ONE DEVICE TYPE
                break
            self.symbol = self.scanner.get_symbol()


    def parse_network(self)->bool:
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.EOF:
            # TODO: RAISE EXCEPTION FOR EMPTY FILE
            return False

        self.parse_devices()
        self.parse_connections()
        self.parse_monitors()
        return self.error_handler.error_count == 0


if __name__ == "__main__":
    #Handler example usage
    error_handler = ErrorHandler()

    error_handler.register_error(100, "Invalid input: {{value}}")
    error_handler.register_error(200, "File not found: {{filename}}")

    error_handler.log_error(100, value=42)
    error_handler.log_error(200, filename="data.txt")
    error_handler.log_error(300, "Unknown error")  # Not registered

    print(f"Total errors logged: {error_handler.get_error_count}")