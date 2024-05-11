"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""

SYMBOL_TYPES = ["NAME","DIGIT","PUNCTUATION",""]
NAMES_SYMBOLS = ["DEVICES","CONNECTIONS","MONITOR"]
PUNCTUATION_SYMBOLS = [">",".",",",'"',";","="]
END_SYMBOL = ""
KEYWORDS = []
LETTERS=["a","A","b","B"]
DIGITS=[f"{i}" for i in range(10)]


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

    def skip_spaces(self):
        pass

    def get_name(self):
        pass

    def get_number(self):
        pass

    def advance(self):
        pass

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        self.skip_spaces()  # current character now not whitespace

        if self.current_character.isalpha():  # name
            name_string = self.get_name()
            if name_string in self.keywords_list:
                symbol.type = self.KEYWORD
            else:
                symbol.type = self.NAME
                [symbol.id] = self.names.lookup([name_string])

        elif self.current_character.isdigit():  # number
            symbol.id = self.get_number()
            symbol.type = self.NUMBER

        elif self.current_character == "=":  # punctuation
            symbol.type = self.EQUALS
            self.advance()

        elif self.current_character == ",":
            # etc for other punctuation
            pass

        elif self.current_character == "":  # end of file
            symbol.type = self.EOF

        else:
            # not a valid character
            self.advance()

        return symbol


    def print_line_error(self):
        pass
