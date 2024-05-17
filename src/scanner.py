"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""

class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """
    def __init__(
            self,
            type:str=None,
            id:int=None,
            line:int=None,
            line_position:int=None
    ):
        """Initialise symbol properties."""
        self.type = type
        self.id   = id
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

    def __init__(self, path, names, devices, keywords):
        """Open specified file and initialise reserved words and IDs."""
        """
        keywords_set = { "DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I" }
        devices_set = {"CLOCK", "SWITCH", "AND", "NAND","CLK","OR", "NOR", "XOR"}
        """

        self.current_character = ""

        self.names = names

        self.devices = devices

        self.keywords = keywords

        self.digits = [ str(i) for i in range(10) ]

        self.symbol_type_list = [
            self.KEYWORD, self.NAME, self.NUMBER, self.DEVICE,
            self.EOF, self.GREATER, self.DOT, self.COMMA,
            self.QUOTE, self.SEMICOL, self.EQUAL
        ] = ["KEYWORD" ,"NAME", "DEVICE" , "NUMBER" ,
             "EOF", "GREATER",  "DOT", "COMMA",
             "QUOTE", "SEMICOL", "EQUAL"
             ]

        self.current_line: int = 1
        self.checkpoint: int = 0 # start of the current line location (to seek to that position)
        self.current_line_position: int = 0

        self.symbols:list = []
        self.file = open(path, "r")

    def get_next_character(self):
        """Read and return the next character in input_file."""
        char = self.file.read(1)
        self.current_line_position += 1
        if char == "\n":
            # char = self.file.read(1) # Enable if you want to get rid of linespaces
            self.current_line += 1
        self.current_character = char
        return char

    def skip_spaces(self):
        while True:
            ch = self.get_next_character()
            if ch != " " or ch == "":
                break

    def get_number(self):
        number = ""
        while self.current_character.isdigit():
            number = number + self.current_character
            self.current_character = self.get_next_character()
        return number

    def get_name(self):
        assert (len(self.current_character)==1 and isinstance(self.current_character, str))
        name = ""
        while self.current_character.isalnum():
            name = name + self.current_character
            self.current_character = self.get_next_character()
        return name

    def advance(self):
        pass

    def create_symbol(self, string, column_pos, line_pos):
        symbol_id = self.names.lookup([string])[0]  # Lookup requires a list
        symbol = Symbol(string, symbol_id, line_pos, column_pos)
        return symbol


    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""

        symbol = Symbol()
        self.skip_spaces()  # current character now not whitespace
        # First check the location-modifying symbols

        if self.current_character == "#":
            # This is a 1-row comment. Ignore this line.
            while self.current_character != "\n" and self.current_character != "":
                self.current_character = self.get_next_character()
            if self.current_character == "\n":
                self.current_character = self.get_next_character()

        elif self.current_character == ";":
            # This is the marker for end of line
            symbol.type = self.SEMICOL
            self.checkpoint = 1 + self.file.tell()

        # Now check the symbol coming after
        if self.current_character.isalpha():  # name
            name_string = self.get_name()
            if self.keywords.query(name_string) is not None:
                symbol.type = self.KEYWORD
                [symbol.id] = self.keywords.query(name_string)

            elif self.devices.query(name_string) is not None:
                symbol.type = self.DEVICE
                [symbol.id] = self.devices.query([name_string])
            else:
                symbol.type = self.NAME
                [symbol.id] = self.names.lookup([name_string])

        elif self.current_character.isdigit():  # number
            symbol.type = self.NUMBER
            symbol.id = self.get_number()

        elif self.current_character == "=":
            symbol.type = self.EQUAL
            self.advance()

        elif self.current_character == ",":
            # etc for other punctuation
            symbol.type = self.COMMA
            self.advance()

        elif self.current_character == ">":
            # etc for other punctuation
            symbol.type = self.GREATER
            self.advance()

        elif self.current_character == ".":
            symbol.type = self.DOT
            self.advance()

        elif self.current_character =='"':
            symbol.type = self.QUOTE
            self.advance()

        elif self.current_character == "":  # end of file
            symbol.type = self.EOF

        else:
            # not a valid character, raise error
            self.print_line_error()
            raise SyntaxError(f"Character {self.current_character} not valid.")

        return symbol

    def get_all_symbols(self, cache=False):
        self.file.seek(0)
        symbols = [self.get_symbol()]
        while symbols[-1].type != self.EOF:
            symbols.append(self.get_symbol())
        if cache:
            self.symbols = symbols
        return symbols

    def print_line_error(self):
        #line starts at self.checkpoint and error occurs at self.current_line_position-self checkpoint spaces away
        temp = self.file.tell()
        self.file.seek(self.checkpoint)
        print(self.file.readline())
        print(" " * (self.current_line_position-self.checkpoint) + "^")
        self.file.seek(temp) #Go back to the error location

if __name__=="__main__":
    import os
    from names import Names
    scanner = Scanner(
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "doc", "net_definition", "circuit1.txt")),
        names = Names(),
        devices= Names(["CLOCK", "SWITCH", "AND", "NAND","CLK","OR", "NOR", "XOR"]),
        keywords=Names(["DEVICES", "CONNECTIONS", "MONITOR", "DATA", "SET", "CLEAR", "Q", "QBAR","I"])
    )
    print([scanner.get_next_character() for _ in range(40)])
