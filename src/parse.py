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
from typing import Optional,Union, Dict, List, Tuple

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

        self.devices_defined: Dict = {}
        self.device_types: List = []

        self.out_ports:List[Tuple[str,Union[str,int]]] = []
        self.connections_defined:List = []

        self.monitors_defined:List = []
        self.counter:int = 0

    def decode(self)->Union[str,None]:
        if self.symbol is None:
            return None
        return self.scanner.decode(self.symbol)
    def detect(self, string: str, type_sym: str)->bool:
        if self.decode() != string:
            return False
        if self.symbol.type != type_sym:
            return False
        return True
    def next_symbol(self)->bool:
        # Returns False if EOF symbol is detected and True otherwise
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
        Returns:
            - True: next line successfully reached
            - False: there was an unexpected keyword
            - None: there was an unexpected EOF
        """
        #Skip to the following line, abort parsing in this line
        if self.symbol is None:
            return None

        while not self.detect(";", self.scanner.PUNCT):
            if self.symbol.type == self.scanner.KEYWORD:
                return False
            if not self.next_symbol(): #Check EOF char
                return None
        return True
    def next_block(self):
        """
        Returns:
            - True: next line successfully reached
            - None: there was an unexpected EOF
        """
        # Skip to the next block, abort parsing in this block
        if self.symbol is None:
            return None
        while self.symbol.type != self.scanner.KEYWORD:
            if not self.next_symbol():
                return None
        return True
    def _device_name(self)->Union[bool,None]:
        """
        EBNF: (alpha | "_"), {alpha | digit | "_" } ;
        :return:
            - True for successful parsing
            - False for unexpected keyword
            - None for unexpected EOF
        """

        if self.symbol.type != self.scanner.NAME:
            self.error_handler.log_error(5,0)
            self.scanner.print_line_error()
            return False

        dev_name = self.decode()
        if dev_name in self.devices_defined:
            ##TODO HANDLE SEMANTIC ERROR: WILL IT BE OVERRIDEN?!?
            self.error_handler.log_error(11,0)

        self.devices_defined[dev_name] = self.counter

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        elif self.symbol != self.scanner.PUNCT:
            self.error_handler.log_error(5,0)
            return False

        while self.decode() == ",":
            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

            elif self.symbol.type != self.scanner.NAME:
                self.error_handler.log_error(5, 0)
                self.scanner.print_line_error()
                return False

            dev_name = self.decode()
            if dev_name in self.devices_defined:
                ##TODO HANDLE SEMANTIC ERROR: WILL IT BE OVERRIDEN?!?
                self.error_handler.log_error(11, 0)

            self.devices_defined[dev_name] = self.counter

            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

            elif self.symbol != self.scanner.PUNCT:
                self.error_handler.log_error(5, 0)
                self.scanner.print_line_error()
                return False

        if not self.detect("=",self.scanner.PUNCT):
            self.error_handler.log_error(5, 0)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        return True
    def _device_type(self) ->Union[bool,None]:
        """
        EBNF:
        device type = ("CLOCK",parameter) | ("SWITCH", parameter) |
                      ("AND", parameter) | ("NAND", parameter) |
                      ("OR", parameter) | ("NOR", parameter) |
                       "XOR" | "DTYPE" ;
              parameter = "[", digit, {digit}, "]" ;
        :return:
            - True for successful parsing
            - False for unexpected keyword
            - None for unexpected EOF
        """

        if self.symbol.type != self.scanner.DEVICE:
            self.error_handler.log_error(5,0)
            return False

        device_type = self.decode()

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        parameter = None

        if device_type in {"CLOCK","SWITCH","AND","NAND","OR","NOR"}: # PARAMETER REQUIRED

            if self.decode()!="[":
                self.error_handler.log_error(6,0)
                return False

            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

            elif self.symbol != self.scanner.NUMBER:
                self.error_handler.log_error(5, 0)
                self.scanner.print_line_error()
                return False

            parameter = self.symbol.id

            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

            elif self.decode()!="]":
                self.error_handler.log_error(1, 0)
                self.scanner.print_line_error()
                return False

            self.device_types.append((device_type,parameter))

            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

        self.device_types.append((device_type, parameter))

        if self.decode() != ";":
            self.error_handler.log_error(2, 0)
            return False

        return True
    def _device_def(self)->Union[bool,None]:
        """
        EBNF:
        device_def = device_name, {",", device_name}, "=", device_type, ";" ;
                    <-------------- _device_name ------->  <--_device_type-->
        :return:
            -True if device definition is successful
            -False for unexpected keyword
            -None for unexpected EOF
        """

        name_check = self._device_name()
        if name_check is None: #unexpected EOF
            self.error_handler.log_error(7,0)
            return None
        elif not name_check: #unexpected keyword
            self.error_handler.log_error(7, 0)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        type_check = self._device_type()

        if type_check is None: #unexpected EOF
            self.error_handler.log_error(7,0)
            return None
        elif not type_check: #unexpected keyword
            self.error_handler.log_error(7, 0)
            return False
        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        return True
    def parse_devices(self)->Union[bool,None]:
        """
        EBNF:
        devices = "DEVICES", ":" , device_def , { device_def } ;
        :returns:
            -True: If there are no errors
            -False: If there is an error
            -None: If unexpected EOF
        """
        # Check for EOF
        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None
        # Handle the case when the start word is not DEVICES
        elif not self.detect("DEVICES", self.scanner.KEYWORD):
            self.error_handler.log_error(1,0)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        elif self.decode()!=":":
            self.error_handler.log_error(2,0)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        self.counter = 0

        line_def = self._device_def()

        if line_def is None: # Unexpected EOF
            self.error_handler.log_error(7,0)
            return None

        elif not line_def: #If there are errors, try the next line
            next_line_def = self.next_line()
            if next_line_def is None: # flag the eof
                self.error_handler.log_error(3,0)
                return None
            elif not next_line_def: # unexpected keyword encountered
                self.error_handler.log_error(4,0)
                return False

            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

        while not self.detect("CONNECTIONS", self.scanner.KEYWORD):

            line_def = self._device_def()

            if line_def is None:  # Unexpected EOF
                self.error_handler.log_error(7, 0)
                return None

            elif not line_def: # Unexpected keyword
                next_line_def = self.next_line()

                if next_line_def is None:  # flag the eof
                    self.error_handler.log_error(3, 0)
                    return None
                elif not next_line_def:  # unexpected keyword encountered
                    self.error_handler.log_error(4, 0)
                    return False

                if not self.next_symbol():
                    self.error_handler.log_error(7, 0)
                    return None

            self.counter += 1

        return True
    def _connection_def(self)-> Union[bool,None]:
        """
        EBNF:
        connection_def = (out_port, ">", in_port), ";" ;
        in_port = device_name , "." , ( "DATA" | "CLK" | "SET" | "CLEAR" | ( "I", digit, {digit} )  ) ;
        out_port = device_name , [".",("Q"|"QBAR")] ;

        :return:
        """

        if self.symbol.type != self.scanner.NAME:
            self.error_handler.log_error(1,1)
            return False

        #Check the device is defined
        out_pin = self.decode()

        #TODO SEMANTIC ERROR
        if out_pin not in self.devices_defined:
            self.error_handler.log_error(0,1)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 1)
            return None

        out_pin_arg=None
        # Check the case when the output port needs arguments
        if self.device_types[self.devices_defined[out_pin]][0] == "DTYPE":
            if self.decode() != ".":
                self.error_handler.log_error(7, 1)
                return False

            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

            if not( self.decode() in {"Q","QBAR"} and self.symbol.type==self.scanner.KEYWORD):
                self.error_handler.log_error(7, 1)
                return False

            out_pin_arg = self.decode()
            self.out_ports.append((out_pin,out_pin_arg))
            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

        if self.decode()!=">":
            self.error_handler.log_error(6,1)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        in_pin = self.decode()

        if in_pin not in self.devices_defined:
            self.error_handler.log_error(0,1)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        elif self.decode()!=".":
            self.error_handler.log_error(6, 1)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 2)
            return None

        elif self.symbol.type != self.scanner.KEYWORD:
            self.error_handler.log_error(4, 1)
            return False

        # Check the case when the input port needs arguments
        if self.device_types[self.device_types[self.devices_defined[in_pin]][0]] == "DTYPE":
            in_pin_arg = self.decode()
            if in_pin_arg not in {"DATA", "CLK", "SET", "CLEAR"}:
                self.error_handler.log_error(8,1)
                self.scanner.print_line_error()
                return False
        else:
            if not self.detect("I", self.scanner.KEYWORD):
                self.error_handler.log_error(3,1)
                return False

            if not self.next_symbol():
                self.error_handler.log_error(7, 1)
                return None
            elif self.symbol.type != self.scanner.NUMBER:
                self.error_handler.log_error(4,1)
                return False

            in_pin_arg = self.symbol.id

        self.connections_defined.append(((out_pin,out_pin_arg), (in_pin,in_pin_arg)))

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        elif not self.detect(";",self.scanner.PUNCT):
            self.error_handler.log_error(4, 1)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 1)
            return None

        return True
    def parse_connections(self)->Union[bool,None]:
        """
        EBNF:
        connections = "CONNECTIONS", ":", {connection_def}, ";" ;
        :return:
            -True: If there are no errors
            -False: If there is an error
            -None: If unexpected EOF
        """
        #Handle the case when the start word is not CONNECTIONS
        if not self.detect( "CONNECTIONS",self.scanner.KEYWORD):
            self.error_handler.log_error(1,0)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        elif self.decode()!=":":
            self.error_handler.log_error(2,0)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        while not self.detect("MONITORS", self.scanner.KEYWORD):
            con = self._connection_def()
            if con is None:
                return None

            elif not con:  # If there are errors, try the next line
                next_line_def = self.next_line()
                if next_line_def is None:  # flag the eof
                    self.error_handler.log_error(3, 1)
                    return None

                elif not next_line_def:  # unexpected keyword encountered
                    self.error_handler.log_error(4, 1)
                    return False

                if not self.next_symbol():
                    self.error_handler.log_error(7, 1)
                    return None

        return True
    def parse_monitors(self)->Union[bool,None]:
        """
        EBNF:
        monitors = "MONITOR", ":", {monitor_def} ;
        monitor_def = output_port, {output_port} ;

        :return:
        """
        if self.symbol is None:
            return True

        elif not self.detect("MONITORS",self.scanner.KEYWORD):
            self.error_handler.log_error(7,2)
            self.scanner.print_line_error()
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 2)
            return None

        elif self.decode() != ":":
            self.error_handler.log_error(2,2)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        monitor = self.decode()

        if monitor not in self.devices_defined:
            self.error_handler.log_error(9,2)
            return False

        if not self.next_symbol():
            self.error_handler.log_error(7, 0)
            return None

        elif self.symbol.type != self.scanner.PUNCT:
            self.error_handler.log_error(1, 2)
            self.scanner.print_line_error()
            return False

        param=None
        if self.decode() == ".":
            if not self.next_symbol():
                self.error_handler.log_error(7, 2)
                return None
            param = self.decode()
            if param not in {"Q","QBAR"}:
                self.error_handler.log_error(3, 2)
                return False
            if not self.next_symbol():
                self.error_handler.log_error(7, 2)
                return None
            elif self.symbol.type != self.scanner.PUNCT:
                self.error_handler.log_error(1, 2)
                self.scanner.print_line_error()
                return False

        self.monitors_defined.append((monitor,param))


        # Iterate over all possible monitor points(output ports of devices)
        while self.detect(",", self.scanner.PUNCT):

            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

            monitor = self.decode()

            if monitor not in self.devices_defined:
                self.error_handler.log_error(9, 2)
                return False

            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

            elif self.symbol.type != self.scanner.PUNCT:
                self.error_handler.log_error(1, 2)
                self.scanner.print_line_error()
                return False

            param=None
            if self.decode() == ".":
                if not self.next_symbol():
                    self.error_handler.log_error(7, 2)
                    return None
                param = self.decode()
                if param not in {"Q","QBAR"}:
                    self.error_handler.log_error(3, 2)
                    return False
                if not self.next_symbol():
                    self.error_handler.log_error(7, 2)
                    return None
                elif self.symbol.type != self.scanner.PUNCT:
                    self.error_handler.log_error(1, 2)
                    self.scanner.print_line_error()
                    return False

            self.monitors_defined.append((monitor,param))
            if not self.next_symbol():
                self.error_handler.log_error(7, 0)
                return None

        if not self.detect(";",self.scanner.PUNCT):
            self.error_handler.log_error(5, 0)
            self.scanner.print_line_error()
            return False

        return True
    def parse_network(self)->bool:
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

        if self.next_symbol():
            self.error_handler.log_error(7, 0)
            return False

        return True
    def create_device(self):
        pass
    def create_connection(self):
        pass
    def create_monitor(self):
        pass
