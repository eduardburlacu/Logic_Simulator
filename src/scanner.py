"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
from typing import Optional
from typeguard import typechecked
class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    @typechecked
    def __init__(
            self,
            type_sym: Optional[str]=None,
            id_sym: Optional[int]=None,
            line: Optional[int]=None,
            line_position: Optional[int]=None
    ):
        """Initialise symbol properties."""
        self.type = type_sym
        self.id   = id_sym
        self.line = line
        self.line_position = line_position


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path:str, names, devices, keywords, punct):
        """Open specified file and initialise reserved words and IDs."""
        """
        keywords_set = { "DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I" }
        devices_set = {"CLOCK", "SWITCH", "AND", "NAND","CLK","OR", "NOR", "XOR"}
        """

        self.current_character = None

        self.names_map = names

        self.devices_map = devices

        self.keywords_map = keywords

        self.punct_map = punct

        self.symbol_type_list = [
            self.KEYWORD, self.NAME, self.NUMBER, self.DEVICE,
            self.EOF, self.PUNCT
        ] = [ "KEYWORD", "NAME",
              "NUMBER", "DEVICE",
              "EOF", "PUNCT" ]

        self.current_line: int = 1
        self.checkpoint: int = 0 # start of the current line location (seek to that position)
        self.current_line_position: int = 0

        self.symbols:list = []
        self.file = open(path, "r")

    def get_next_character(self):
        """Read and return the next character in input_file."""
        char = self.file.read(1)
        self.current_line_position += 1
        if char == "\n":
            self.current_line += 1
        self.current_character = char
        return char

    def skip_spaces(self):
        while self.current_character in {" ","\n","\t",None} and self.current_character != "":
            self.get_next_character()

    def get_number(self)->str:
        number = ""
        while self.current_character.isdigit():
            number = number + self.current_character
            self.current_character = self.get_next_character()
        return number

    def get_name(self):
        assert (len(self.current_character)==1 and isinstance(self.current_character, str))
        name = ""
        while self.current_character.isalnum() or self.current_character=="_":
            name = name + self.current_character
            self.current_character = self.get_next_character()
        return name


    @typechecked
    def create_symbol(self, string:str, type_sym:str):
        if type_sym==self.EOF:
            symbol_id = 0
        elif type_sym==self.PUNCT:
            symbol_id = self.punct_map.query(string)
        elif type_sym==self.NAME:
            [symbol_id] = self.names_map.lookup([string])
        elif type_sym==self.DEVICE:
            symbol_id = self.devices_map.query(string)
        elif type_sym==self.KEYWORD:
            symbol_id = self.keywords_map.query(string)
        elif type_sym==self.NUMBER:
            symbol_id = int(string)
        else:
            raise AttributeError("Unsupported symbol type")

        return Symbol(
            type_sym=type_sym,
            id_sym= symbol_id,
            line=self.current_line,
            line_position = self.current_line_position
        )

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""

        # First check the location-modifying symbols and go to the next symbol head
        self.skip_spaces()  # current character now not whitespace
        if self.current_character == "#":
            # This is a 1-row comment. Ignore this line.
            while self.current_character != "\n" and self.current_character != "":
                self.current_character = self.get_next_character()
            if self.current_character == "\n":
                self.current_character = self.get_next_character()
                self.skip_spaces()


        # Now check the symbol coming after
        if self.current_character in {";",":"}:
            # This is the marker for end of statement
            symbol = self.create_symbol(self.current_character, self.PUNCT)
            self.checkpoint = 1 + self.file.tell()
            self.get_next_character()
            self.skip_spaces()

        elif self.current_character.isalpha() or self.current_character=="_":  # name
            name_string = self.get_name()
            if self.keywords_map.query(name_string) is not None:
                symbol =self.create_symbol(name_string, self.KEYWORD)

            elif self.devices_map.query(name_string) is not None:
                symbol = self.create_symbol(name_string, self.DEVICE)

            else:
                symbol = self.create_symbol(name_string, self.NAME)

        elif self.current_character.isdigit():  # number
            number = self.get_number()
            symbol = self.create_symbol(number, self.NUMBER)

        elif self.punct_map.query(self.current_character) is not None:
            symbol = self.create_symbol(self.current_character, self.PUNCT)
            self.get_next_character()

        elif self.current_character == "":  # end of file
            symbol = self.create_symbol(self.current_character,self.EOF)

        else:
            # not a valid character, raise error
            self.print_line_error()
            raise SyntaxError(f"Character {self.current_character} not valid.")
        print(symbol.type,symbol.id)
        return symbol

    def get_all_symbols(self, cache=False):
        self.file.seek(0)
        symbols = []
        while True:
            symbol = self.get_symbol()
            symbols.append(symbol)
            if symbols[-1].type == self.EOF:
                break

        if cache:
            self.symbols = symbols

        return symbols

    def print_line_error(self):
        #line starts at self.checkpoint and error occurs at self.current_line_position-self checkpoint spaces away
        temp = self.file.tell()
        self.file.seek(self.checkpoint)
        print("\n")
        print(self.file.readline()[:-1])
        print(" " * (self.current_line_position-self.checkpoint) + "^")
        self.file.seek(temp) #Go back to the error location

