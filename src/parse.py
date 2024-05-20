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
from typing import Optional,Union, Dict, List

class ErrorHandler:
    def __init__(self):
        self.error_code_map:Dict = {}
        self.error_count: List[int] = [0,0,0]
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

    @property
    def get_error_count(self,idx:Optional[int]=None)->int:
        if idx is None:
            return sum(self.error_count)
        elif idx in {0,1,2}:
            return self.error_count[idx]
        else:
            raise AttributeError(f"error_count getter has an invalid idx:{idx}")

    def register_error(
            self,
            error_code:Union[int,List[int]],
            error_msg:Union[str,List[str]]
    ):

        if not isinstance(error_code, int):
            raise ValueError("Error code must be an integer")
        self.error_code_map[error_code] = error_msg

    def log_error(self, error_code:int, idx:int,*args,**kwargs):
        """
        Handles an error by logging it.
        Args:
            error_code (int): The error code to log.
            idx (int): One element of {0,1,2}. Encodes if the error is produced
                       in DEVICES, CONNECTIONS, respectively MONITORS
            *args: Additional arguments to be logged with the error message.
            **kwargs: Additional keyword arguments to be logged with the error message.
        """
        if error_code not in self.error_code_map:
            self.logger.error(f"Unknown error code: {error_code}")

        error_message = self.error_code_map[error_code].format(*args, **kwargs)
        self.logger.error(error_message)
        self.error_count[idx] += 1


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
        self.scanner.file.seek(0)
        self.error_handler= ErrorHandler()
        self.symbol: Union[Symbol,None] = self.scanner.get_symbol()
        self.prev_symbol: Union[Symbol,None] = None

    def decode(self)->Union[str,None]:
        if self.symbol is None:
            return None
        return self.scanner.decode(self.symbol)

    def detect(self, string: str, type_sym: str)->bool:
        if self.decode() != string:
            return False
        if self.symbol.type == type_sym:
            return True
        return False

    def next_symbol(self):
        if self.symbol.type == self.scanner.EOF:
            self.prev_symbol = self.symbol
            self.symbol = None
        else:
            self.prev_symbol = self.symbol
            self.symbol = self.scanner.get_symbol()

    def _device_name(self)->bool:
        """
        EBNF: (alpha | "_"), {alpha | digit | "_" } ;
        """
        if self.symbol is None:
            self.error_handler.log_error(1,0)
            self.scanner.print_line_error()
            return False
        elif self.symbol.type != self.scanner.NAME:
            self.error_handler.log_error(5,0)
            self.scanner.print_line_error()
            return False
        devices_defined = [self.decode()]
        self.next_symbol()
        if self.symbol is None:
            self.error_handler.log_error(7, 0)
            return False
        elif self.symbol != self.scanner.PUNCT:
            self.error_handler.log_error(5,0)
            return False

        while self.decode() == ",":
            self.next_symbol()
            if self.symbol is None:
                self.error_handler.log_error(7, 0)
                return False
            elif self.symbol.type != self.scanner.NAME:
                self.error_handler.log_error(5, 0)
                self.scanner.print_line_error()
                return False

            devices_defined.append(self.decode())

            self.next_symbol()
            if self.symbol is None:
                self.error_handler.log_error(7, 0)
                self.scanner.print_line_error()
                return False
            elif self.symbol != self.scanner.PUNCT:
                self.error_handler.log_error(5, 0)
                self.scanner.print_line_error()
                return False

        if self.decode() != "=":
            self.error_handler.log_error(5, 0)
            self.scanner.print_line_error()
            return False
        # TODO: when integrating devices, the list devices_defined can be used to interface with those
        return True


    def _device_type(self) ->bool:
        """
        EBNF: device type = ("CLOCK",parameter) | ("SWITCH", parameter) |
                            ("AND",parameter) | ("NAND", parameter) |
                            ("OR", parameter) | ("NOR", parameter) |
                             "XOR" | "DTYPE" ;
              pameter = "[", digit, {digit}, "]" ;
        :return:
        """
        if self.symbol is None:
            self.error_handler.log_error(1,0)
            self.scanner.print_line_error()
            return False

        elif self.symbol.type != self.scanner.DEVICE:
            self.error_handler.log_error(5,0)
            self.scanner.print_line_error()
            return False

        device_type = self.decode()

        self.next_symbol()

        if self.symbol is None:
            self.error_handler.log_error(1,0)
            self.scanner.print_line_error()
            return False

        if device_type not in {"XOR","DTYPE"}: # PARAMETER REQUIRED

            if self.decode()!="[":
                self.error_handler.log_error(6,0)
                return False

            self.next_symbol()

            if self.symbol is None:
                self.error_handler.log_error(1, 0)
                self.scanner.print_line_error()
                return False
            elif self.symbol != self.scanner.NUMBER:
                self.error_handler.log_error(5, 0)
                self.scanner.print_line_error()
                return False

            parameter: int = self.symbol.id

            self.next_symbol()

            if self.symbol is None:
                self.error_handler.log_error(1, 0)
                self.scanner.print_line_error()
                return False

            elif self.decode()!="]":
                self.error_handler.log_error(1, 0)
                self.scanner.print_line_error()
                return False

            self.next_symbol()
            if self.symbol is None:
                self.error_handler.log_error(1, 0)
                self.scanner.print_line_error()
                return False

        if self.decode() != ";":
            self.error_handler.log_error(2, 0)
            self.scanner.print_line_error()
            return False
        # TODO: device_type or (device_type,paramter) will be passed to devices
        return True


    def parse_devices(self)->bool:
        """
        EBNF:
        devices = "DEVICES", ":" , device_def , { device_def } ;
        device_def = device_name, {",", device_name}, "=", device_type, ";" ;
        :return:
        """
        #Handle the case when the start word is not DEVICES
        if not self.detect("DEVICES",self.scanner.KEYWORD):
            self.error_handler.log_error(1,0)
            self.scanner.print_line_error()
            return False

        self.next_symbol()

        if self.symbol is None:
            self.error_handler.log_error(1,0)
            self.scanner.print_line_error()
            return False
        elif self.decode()!=":":
            self.error_handler.log_error(2,0)
            self.scanner.print_line_error()

        self.next_symbol()

        while True:

            self._device_name()
            self.next_symbol()
            self._device_type()
            self.next_symbol()

            if self.detect("CONNECTIONS", self.scanner.KEYWORD):
                return self.error_handler.error_count[0]==0

            elif self.symbol is None:  #Unexpected EOF
                self.error_handler.log_error(3,0)
                self.scanner.print_line_error()
                return False


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
        self.next_symbol()
        self.parse_devices()
        self.parse_connections()
        self.parse_monitors()
        return self.error_handler.error_count == 0


if __name__ == "__main__":
    #Handler example usage
    error_handler = ErrorHandler()
    error_handler.register_error(100, "Invalid input: {{value}}")
    error_handler.register_error(200, "File not found: {{filename}}")
    error_handler.log_error(100, 0)
    error_handler.log_error(200, 1)
    print(f"Total errors logged: {error_handler.get_error_count}")

