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
from typing import Optional, Union, Dict, List, Tuple
from custom_errors import SemanticErrorsC, SyntaxErrorsC


class ErrorHandler:
    """Handles Errors for the Parser."""

    def __init__(self):
        """Initialise the error code count, and logger."""
        self.error_count: List[int] = [0, 0, 0]
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

    @property
    def get_error_count(self, idx: Optional[int] = None) -> int:
        """Return the total amount of errors, or errors in each section."""
        if idx is None:
            return sum(self.error_count)
        elif idx in {0, 1, 2}:
            return self.error_count[idx]
        else:
            raise AttributeError(
                f"error_count getter has an invalid idx:{idx}"
                )

    def log_error(
            self, error_type: str, error_code: int, idx: int, *args, **kwargs
            ):
        """
        Handle the error by logging it.

        Args:
            error_code (int): The error code to log.
            idx (int):  One element of {0, 1, 2}.
                        Encodes if the error is produced in DEVICES,
                        CONNECTIONS, MONITORS respectively.
            s (Scanner): The scanner of the parser
            *args: Additional arguments to be logged with the error message.
            **kwargs: Additional keyword arguments to be
                      logged with the error message.
        """
        print(f"Error encountered: {error_code}, {idx}")
        self.error_count[idx] += 1

        if error_type == "Syn":
            if error_code == 1:
                with SyntaxErrorsC.CharNotSupported(idx) as e:
                    print(e)
            elif error_code == 2:
                with SyntaxErrorsC.DigitStartsName(idx) as e:
                    print(e)
            elif error_code == 3:
                with SyntaxErrorsC.MultipleAssignments(idx) as e:
                    print(e)
            elif error_code == 4:
                with SyntaxErrorsC.ParameterLetter(idx) as e:
                    print(e)
            elif error_code == 5:
                with SyntaxErrorsC.UnexpectedEOF(idx) as e:
                    print(e)
            elif error_code == 6:
                with SyntaxErrorsC.InvalidSymbol(idx) as e:
                    print(e)
            elif error_code == 7:
                with SyntaxErrorsC.UnexpectedKeyword(idx) as e:
                    print(e)
            elif error_code == 8:
                with SyntaxErrorsC.InvalidPunct(idx) as e:
                    print(e)
            else:
                raise ValueError("Invalid Error Code for Syntax")
        if error_type == "Sem":
            if error_code == 1:
                with SemanticErrorsC.InputNotAssigned(idx) as e:
                    print(e)
            elif error_code == 2:
                with SemanticErrorsC.InputToSwitchAssigned(idx) as e:
                    print(e)
            elif error_code == 3:
                with SemanticErrorsC.ClockPeriodZero(idx) as e:
                    print(e)
            elif error_code == 4:
                with SemanticErrorsC.ReferencedBeforeAssigned(idx) as e:
                    print(e)
            elif error_code == 5:
                with SemanticErrorsC.AlreadyAssigned(idx) as e:
                    print(e)
            elif error_code == 6:
                with SemanticErrorsC.DeviceNameI(idx) as e:
                    print(e)
            elif error_code == 7:
                with SemanticErrorsC.MonitorOnInput(idx) as e:
                    print(e)
            elif error_code == 8:
                with SemanticErrorsC.DeviceNotExist(idx) as e:
                    print(e)
            elif error_code == 9:
                with SemanticErrorsC.PinNotExist(idx) as e:
                    print(e)
            else:
                raise ValueError("Invalid Error Code for Semantic")
        else:
            raise TypeError("Invalid Error Type")


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

        self.error_handler = ErrorHandler()

        self.symbol: Union[Symbol, None] = self.scanner.get_symbol()
        self.prev_symbol: Union[Symbol, None] = None

        self.devices_defined: Dict = {}
        self.device_types: List = []

        self.out_ports: List[Tuple[str, Union[str, int]]] = []
        self.connections_defined: List = []

        self.monitors_defined: List = []
        self.counter: int = 0

    def decode(self) -> Union[str, None]:
        """Decode the current symbol."""
        if self.symbol is None:
            return None
        return self.scanner.decode(self.symbol)

    def detect(self, string: str, type_sym: str) -> bool:
        """Check whether the decoding was successful."""
        if self.decode() != string:
            return False
        if self.symbol.type != type_sym:
            return False
        return True

    def next_symbol(self) -> bool:
        """
        Move to the next symbol provided.

        Returns False if EOF symbol is detected and True otherwise.
        """
        if self.symbol.type == self.scanner.EOF:
            self.prev_symbol = self.symbol
            self.symbol = None
            return False
        else:
            self.prev_symbol = self.symbol
            self.symbol = self.scanner.get_symbol()
            return True

    def next_line(self):
        """
        Return the following.

            - True: next line successfully reached
            - False: there was an unexpected keyword
            - None: there was an unexpected EOF
        """
        #  Skip to the following line, abort parsing in this line
        if self.symbol is None:
            return None

        while not self.detect(";", self.scanner.PUNCT):
            if self.decode() in {"CONNECTIONS", "MONITORS"}:
                return False
            if not self.next_symbol():
                # Check EOF char
                return None
        return True

    def next_block(self):
        """
        Return.

            - True: next block successfully reached
            - None: there was an unexpected EOF
        """
        #  Skip to the next block, abort parsing in this block
        if self.symbol is None:
            return None
        while self.symbol.type != self.scanner.KEYWORD or self.symbol.id > 2:
            if not self.next_symbol():
                return None
        return True

    def _device_name(self) -> Union[bool, None]:
        """
        Return the following.

            - True for successful parsing
            - False for unexpected keyword
            - None for unexpected EOF
        EBNF: (alpha | "_"), {alpha | digit | "_" } ;
        """
        if self.symbol.type != self.scanner.NAME:
            #  Invalid Symbol Error
            self.error_handler.log_error("Syn", 6, 0)
            self.scanner.print_line_error()
            return False

        dev_name = self.decode()
        if dev_name in self.devices_defined:
            #  TODO HANDLE SEMANTIC ERROR: WILL IT BE OVERRIDEN?!?
            #  Device Already Defined
            self.error_handler.log_error("Sem", 5, 0)
            self.scanner.print_line_error()

        self.devices_defined[dev_name] = self.counter

        if not self.next_symbol():
            # Unexpected EOF
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        elif self.symbol.type != self.scanner.PUNCT:
            # Invalid Punct
            self.error_handler.log_error("Syn", 8, 0)
            self.scanner.print_line_error()
            return False

        while self.decode() == ",":
            if not self.next_symbol():
                # Unexpected EOF
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                return None

            elif self.symbol.type != self.scanner.NAME:
                # Invalid Symbol
                self.error_handler.log_error("Syn", 6, 0)
                self.scanner.print_line_error()
                return False

            dev_name = self.decode()

            if dev_name in self.devices_defined:
                # TODO HANDLE SEMANTIC ERROR: WILL IT BE OVERRIDEN?!?
                # Already Defined
                self.error_handler.log_error("Sem", 5, 0)
                self.scanner.print_line_error()
                return False

            self.devices_defined[dev_name] = self.counter

            if not self.next_symbol():
                # Unexpected EOF
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                return None

            elif self.symbol.type != self.scanner.PUNCT:
                self.error_handler.log_error("Syn", 8, 0)
                self.scanner.print_line_error()
                return False

        if not self.detect("=", self.scanner.PUNCT):
            self.error_handler.log_error("Syn", 8, 0)
            self.scanner.print_line_error()
            return False

        return True

    def _device_type(self) -> Union[bool, None]:
        """
        Return the following.

            - True for successful parsing
            - False for unexpected keyword
            - None for unexpected EOF
        EBNF:
        device type = ("CLOCK", parameter) | ("SWITCH", parameter) |
                      ("AND", parameter) | ("NAND", parameter) |
                      ("OR", parameter) | ("NOR", parameter) |
                       "XOR" | "DTYPE" ;
              parameter = "[", digit, {digit}, "]" ;
        """
        if self.symbol.type != self.scanner.DEVICE:
            #  Invalid Symbol
            self.error_handler.log_error("Syn", 6, 0)
            self.scanner.print_line_error()
            return False

        device_type = self.decode()

        if not self.next_symbol():
            #  Unexpected EOF
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        parameter = None

        if device_type in {
                "CLOCK", "SWITCH", "AND", "NAND", "OR", "NOR"
                }:  # PARAMETER REQUIRED

            if self.decode() != "[":
                self.counter -= 1
                self.devices_defined.pop(list(self.devices_defined)[-1])
                self.error_handler.log_error("Syn", 8, 0)
                self.scanner.print_line_error()
                return False

            if not self.next_symbol():
                # Unexpected EOF
                self.counter -= 1
                self.devices_defined.pop(list(self.devices_defined)[-1])
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                # ^Addition by Nikko, if wrong remove
                return None

            elif self.symbol.type != self.scanner.NUMBER:
                # Parameter Letter Error
                self.counter -= 1
                self.devices_defined.pop(list(self.devices_defined)[-1])
                self.error_handler.log_error("Syn", 4, 0)
                self.scanner.print_line_error()
                return False

            parameter = self.symbol.id

            if not self.next_symbol():
                #  Unexpected EOF
                self.counter -= 1
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                return None

            elif self.decode() != "]":
                self.counter -= 1
                self.devices_defined.pop(list(self.devices_defined)[-1])
                self.error_handler.log_error("Syn", 8, 0)
                #  TODO WHAT ERROR IS THIS?
                self.scanner.print_line_error()
                return False

            if not self.next_symbol():
                #  Unexpected EOF Error
                self.counter -= 1
                self.devices_defined.pop(list(self.devices_defined)[-1])
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                return None

        self.device_types.append((device_type, parameter))

        if self.decode() != ";":
            #  Invalid Punct
            self.error_handler.log_error("Syn", 8, 0)
            self.scanner.print_line_error()
            return False

        return True

    def _device_def(self) -> Union[bool, None]:
        """
        Return the following.

            -True if device definition is successful
            -False for unexpected keyword
            -None for unexpected EOF
        EBNF:
        device_def = device_name, {",", device_name}, "=", device_type, ";" ;
                    <-------------- _device_name ------->  <-_device_type->
        """
        name_check = self._device_name()
        if name_check is None:  # unexpected EOF
            return None
        elif not name_check:  # unexpected keyword
            return False

        if not self.next_symbol():
            # Unexpected EOF
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        type_check = self._device_type()

        if type_check is None:
            # unexpected EOF
            return None
        elif not type_check:
            # unexpected keyword
            return False

        if not self.next_symbol():
            #  Unexpected EOF
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        return True

    def parse_devices(self) -> Union[bool, None]:
        """
        Return the following.

            -True: If there are no errors
            -False: If there is an error
            -None: If unexpected EOF
        EBNF:
        devices = "DEVICES", ":" , device_def , { device_def } ;
        """
        #  Check for EOF
        if self.symbol is None:
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        #  Handle the case when the start word is not DEVICES
        elif not self.detect("DEVICES", self.scanner.KEYWORD):
            #  Invalid Symbol?
            self.error_handler.log_error("Syn", 6, 0)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            #  unexpected EOF
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        elif self.decode() != ":":
            #  Invalid Symbol
            self.error_handler.log_error("Syn", 6, 0)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            #  Unexpected EOF
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        self.counter = 0

        line_def = self._device_def()

        if line_def is None:  # Unexpected EOF
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None
        elif not line_def:  # If there are errors, try the next line
            next_line_def = self.next_line()
            if next_line_def is None:  # flag the eof
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                return None
            elif not next_line_def:  # unexpected keyword encountered
                self.error_handler.log_error("Syn", 7, 0)
                self.scanner.print_line_error()
                return False

            if not self.next_symbol():
                # unexpected EOF
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                return None

        self.counter += 1

        while not self.detect("CONNECTIONS", self.scanner.KEYWORD):

            line_def = self._device_def()

            if line_def is None:  # Unexpected EOF
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                return None

            elif not line_def:  # Unexpected keyword
                next_line_def = self.next_line()

                if next_line_def is None:  # flag the eof
                    self.error_handler.log_error("Syn", 5, 0)
                    self.scanner.print_line_error()
                    return None
                elif not next_line_def:  # unexpected keyword encountered
                    self.error_handler.log_error("Syn", 7, 0)
                    self.scanner.print_line_error()
                    return False

                if not self.next_symbol():
                    self.error_handler.log_error("Syn", 5, 0)
                    self.scanner.print_line_error()
                    return None

            self.counter += 1

        return True

    def _connection_def(self) -> Union[bool, None]:
        """
        Return.

        EBNF:
        connection_def = (out_port, ">", in_port), ";" ;
        in_port = device_name , "." ,
                ( "DATA" | "CLK" | "SET" | "CLEAR"
                | ( "I", digit, {digit} )  ) ;
        out_port = device_name , [".", ("Q"|"QBAR")] ;
        """
        # print(F"________CURRENT SYMBOL
        #      IS {self.decode()} {self.symbol.type} _____")
        if self.symbol.type != self.scanner.NAME:
            self.error_handler.log_error("Syn", 6, 1)
            self.scanner.print_line_error()
            return False

        # Check the device is defined
        out_pin = self.decode()

        # TODO SEMANTIC ERROR
        if out_pin not in self.devices_defined:
            self.error_handler.log_error("Sem", 4, 1)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error("Syn", 5, 1)
            self.scanner.print_line_error()
            return None

        out_pin_arg = None
        # Check the case when the output port needs arguments
        if self.device_types[
                self.devices_defined[out_pin]
                ][0] == "DTYPE":
            if self.decode() != ".":
                self.error_handler.log_error("Syn", 6, 1)
                #  Invalid Symbol for now
                self.scanner.print_line_error()
                return False

            if not self.next_symbol():
                self.error_handler.log_error("Syn", 5, 1)
                self.scanner.print_line_error()
                return None

            if not (self.decode() in {"Q", "QBAR"} and
                    self.symbol.type == self.scanner.KEYWORD
                    ):
                self.error_handler.log_error("Syn", 6, 1)
                # Invalid Symbol?
                self.scanner.print_line_error()
                return False

            out_pin_arg = self.decode()
            self.out_ports.append((out_pin, out_pin_arg))
            if not self.next_symbol():
                self.error_handler.log_error("Syn", 5, 1)
                self.scanner.print_line_error()
                return None

        if self.decode() != ">":
            self.error_handler.log_error("Syn", 8, 1)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error("Syn", 5, 1)
            self.scanner.print_line_error()
            return None

        in_pin = self.decode()

        if in_pin not in self.devices_defined:
            self.error_handler.log_error("Sem", 9, 1)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error("Syn", 5, 1)
            self.scanner.print_line_error()
            return None

        elif self.decode() != ".":
            self.error_handler.log_error("Syn", 8, 1)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error("Syn", 5, 1)
            self.scanner.print_line_error()
            return None
        in_pin_arg = self.decode()

        # Check the case when the input port needs arguments
        if self.device_types[self.devices_defined[in_pin]][0] == "DTYPE":

            if in_pin_arg not in {"DATA", "CLK", "SET", "CLEAR"}:
                self.error_handler.log_error("Sem", 9, 1)
                self.scanner.print_line_error()
                return False
        else:
            # The current symbol is of the form  I + number
            if in_pin_arg[0] != "I":
                self.error_handler.log_error("Syn", 6, 1)
                self.scanner.print_line_error()
                return False
            try:
                in_pin_arg = int(in_pin_arg[1:])
            except ValueError as e:  # invalid input
                self.error_handler.log_error("Sem", 9, 1)
                self.scanner.print_line_error()  # Insert from Nikko
                return False

        self.connections_defined.append(
            ((out_pin, out_pin_arg), (in_pin, in_pin_arg)))
        # TODO MAKE IT CORRESPONDING TO API

        if not self.next_symbol():
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        elif not self.detect(";", self.scanner.PUNCT):
            self.error_handler.log_error("Syn", 8, 1)
            self.scanner.print_line_error()
            return False

        return True

    def parse_connections(self) -> Union[bool, None]:
        """
        Parse through the connection definitions.

        EBNF:
        connections = "CONNECTIONS", ":", {connection_def}, ";" ;
        :return:
            -True: If there are no errors
            -False: If there is an error
            -None: If unexpected EOF
        """
        # Handle the case when the start word is not CONNECTIONS
        if not self.detect("CONNECTIONS", self.scanner.KEYWORD):
            self.error_handler.log_error("Syn", 6, 0)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            #  Unexpected EOF
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        elif self.decode() != ":":
            self.error_handler.log_error("Syn", 8, 0)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        while not self.detect("MONITORS", self.scanner.KEYWORD):
            con = self._connection_def()
            if con is None:
                # unexpected eof
                self.error_handler.log_error("Syn", 5, 1)
                self.scanner.print_line_error()
                return None

            elif not con:  # If there are errors, try the next line
                next_line_def = self.next_line()

                if next_line_def is None:  # flag the eof
                    self.error_handler.log_error("Syn", 5, 1)
                    self.scanner.print_line_error()
                    return None

                elif not next_line_def:  # unexpected keyword encountered
                    self.error_handler.log_error("Syn", 7, 1)
                    self.scanner.print_line_error()
                    return False

            if not self.next_symbol():
                # Here it should be True and not None because the
                # Monitors is not existent(allowed by EBNF) and you reach EOF
                return True

        return True

    def parse_monitors(self) -> Union[bool, None]:
        """
        Parse the monitor definitons.

        EBNF:
        monitors = "MONITOR", ":", {monitor_def} ;
        monitor_def = output_port, {output_port} ;
        """
        if self.symbol is None:
            return True

        elif not self.detect("MONITORS", self.scanner.KEYWORD):
            # Unexpected EOF
            self.error_handler.log_error("Syn", 5, 2)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            # Unexpected EOF
            self.error_handler.log_error("Syn", 5, 2)
            self.scanner.print_line_error()
            return None

        elif self.decode() != ":":
            self.error_handler.log_error("Syn", 8, 2)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()
            return None

        monitor = self.decode()

        if monitor not in self.devices_defined:
            self.error_handler.log_error("Sem", 8, 2)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error("Syn", 5, 0)
            self.scanner.print_line_error()  # Nikko addition, not sure
            return None

        elif self.symbol.type != self.scanner.PUNCT:
            self.error_handler.log_error("Syn", 8, 2)
            self.scanner.print_line_error()
            return False

        param = None

        if self.decode() == ".":
            if not self.next_symbol():
                self.error_handler.log_error("Syn", 8, 2)
                self.scanner.print_line_error()
                return None
            param = self.decode()
            if param not in {"Q", "QBAR"}:
                self.error_handler.log_error("Syn", 6, 2)
                self.scanner.print_line_error()
                return False
            if not self.next_symbol():
                # Unexpected EOF
                self.error_handler.log_error("Syn", 5, 2)
                self.scanner.print_line_error()
                return None
            elif self.symbol.type != self.scanner.PUNCT:
                self.error_handler.log_error("Syn", 8, 2)
                self.scanner.print_line_error()
                return False

        self.monitors_defined.append((monitor, param))

        # Iterate over all possible monitor points(output ports of devices)
        while self.detect(",", self.scanner.PUNCT):

            if not self.next_symbol():
                # Unexpected EOF
                self.error_handler.log_error("Syn", 5, 2)
                self.scanner.print_line_error()
                return None

            monitor = self.decode()

            if monitor not in self.devices_defined:
                self.error_handler.log_error("Sem", 8, 2)
                self.scanner.print_line_error()
                return False

            if not self.next_symbol():
                self.error_handler.log_error("Syn", 5, 0)
                self.scanner.print_line_error()
                return None

            elif self.symbol.type != self.scanner.PUNCT:
                self.error_handler.log_error("Syn", 8, 2)
                self.scanner.print_line_error()
                return False

            param = None
            if self.decode() == ".":

                if not self.next_symbol():
                    self.error_handler.log_error("Syn", 5, 2)
                    self.scanner.print_line_error()
                    return None
                param = self.decode()
                if param not in {"Q", "QBAR"}:
                    self.error_handler.log_error("Syn", 6, 2)
                    self.scanner.print_line_error()
                    return False

                if not self.next_symbol():
                    self.error_handler.log_error("Syn", 5, 2)
                    self.scanner.print_line_error()
                    return None
                elif self.symbol.type != self.scanner.PUNCT:
                    self.error_handler.log_error("Syn", 8, 2)
                    self.scanner.print_line_error()
                    return False

            self.monitors_defined.append((monitor, param))

        if not self.detect(";", self.scanner.PUNCT):
            self.error_handler.log_error("Syn", 8, 0)
            self.scanner.print_line_error()
            return False

        return True

    def parse_network(self) -> bool:
        """Parse the circuit definition file."""
        parsed_devices = self.parse_devices()
        if parsed_devices is None:
            return False
        elif not parsed_devices:
            if not self.next_block():
                return False

        parsed_connections = self.parse_connections()

        if parsed_connections is None:
            return False
        elif not parsed_connections:
            if not self.next_block():
                return False

        parsed_monitors = self.parse_monitors()
        if parsed_monitors is not True:
            return False

        # TODO be more rigorous with handling EOF at the end
        return self.error_handler.error_count == 0

    def create_devices(self):
        """Create device objects from list of device names."""
        for d in self.device_types:
            # d is of form (device_type, parameter)
            errorOut = self.devices.make_device(
                self.device_types[self.devices_defined[d[0]]][0], d[1]
                )
            if errorOut != self.devices.NO_ERROR:
                with ValueError as e:
                    print(e)

    def create_network(self):
        """Create new connection between two devices."""
        for c in self.connections_defined:
            # c is of form  ((out_pin, out_pin_arg), (in_pin, in_pin_arg))
            self.network.make_connection(c[0][0], c[0][1], c[1][0], c[1][1])

    def create_monitors(self):
        """Place a monitor on an output."""
        for m in self.monitors_defined:
            # m is of form (monitor, param)
            self.monitors.make_monitor(m[0], m[1])
