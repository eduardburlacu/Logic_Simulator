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
    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None
        self.line = None
        self.line_position = None



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

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""
        self.current_character = ""

        self.names = names

        self.keywords = [ "DEVICES", "CONNECTIONS", "MONITOR" ]

        self.digits = [ str(i) for i in range(10) ]

        self.punctuation = [">", ".", ",", '"', ";", "=" ]

        self.symbol_type_list = [
            self.KEYWORD,self.NAME,self.NUMBER, self.PUNCTUATION,
            self.EOF, self.GREATER, self.DOT, self.COMMA,
            self.QUOTE, self.SEMICOL, self.EQUAL
        ] = range(11)

        self.letters = ["A", "B", "C", "D", "E", "F", "G"
            , "H", "I", "J", "K", "L", "M", "N"
            , "O", "P", "Q", "R", "S", "T", "U"
            , "V", "W", "X", "Y", "Z", "a", "b"
            , "c", "d", "e", "f", "g", "h", "i"
            , "j", "k", "l", "m", "n", "o", "p"
            , "q", "r", "s", "t", "u", "v", "w"
            , "x", "y", "z"]

        self.end = ""

        # Open the file
        self.input_file = open( path, "r" )

    def get_next_character(self):
        """Read and return the next character in input_file."""
        char = self.input_file.read(1)

        # Enable if you want to get rid of linespaces
        if char == "\n":
            char = self.input_file.read(1)
        return char

    def skip_spaces(self):
        while True:
            ch = self.get_next_character()
            if ch != " " or ch == "":
                return ch

    def skip_comment(self):
        pass

    def get_number(self):
        ch = self.get_next_character()
        number = ""
        while ch != "":
            while ch.isdigit():
                number = number + ch
                ch = self.get_next_character()
            if number != "":
                break
            else:
                ch = self.get_next_character()
        return [number, ch]

    def get_name(self):
        ch = self.get_next_character()
        while not ch.isalpha():
            ch = self.get_next_character()
            if ch == "":
                return [None, ch]
        name = ""
        while ch != "":
            while ch.isalnum():
                name = name + ch
                ch = self.get_next_character()
            if name != "":
                break
            else:
                ch = self.get_next_character()
        if name == "":
            name = None
        return [ name, ch]

    def advance(self):
        pass

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""

        symbol = Symbol()
        self.skip_spaces()  # current character now not whitespace

        if self.current_character.isalpha():  # name
            name_string = self.get_name()
            if name_string in self.keywords:
                symbol.type = self.KEYWORD
            else:
                symbol.type = self.NAME
                [symbol.id] = self.names.lookup( [name_string] )

        elif self.current_character == "#":
            #This is a comment. Ignore this line
            self.skip_comment()

        elif self.current_character.isdigit():  # number
            symbol.id = self.get_number()
            symbol.type = self.NUMBER

        elif self.current_character == "=":  # punctuation
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

        elif self.current_character == ";":
            # etc for other punctuation
            symbol.type = self.SEMICOL


        elif self.current_character == ".":
            symbol.type = self.DOT
            self.advance()

        elif self.current_character =='"':
            symbol.type = self.QUOTE
            self.advance()

        elif self.current_character == "":  # end of file
            symbol.type = self.EOF

        else:
            # not a valid character
            self.advance()

        return symbol


    def print_line_error(self):
        pass
