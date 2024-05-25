"""Define Custom Errors; Syntax and Semanic."""

POSITIONS = ["DEVICES", "CONNECTIONS", "MONITORS"]


# Syntax Errors
class CharNotSupportedError(Exception):
    """Raised when a character is out of the grammar."""

    def __init__(self, pos,
                 message="Syntax Error: Character Not Supported, in: "):
        """Intialise."""
        self.message = message
        self.pos = pos
        super().__init__(self.message + POSITIONS[pos])


class DigitStartsNameError(Exception):
    """Raised when a name is defined that starts with a digit."""

    def __init__(self, pos,
                 message="Syntax Error: Name Cannot Start With A Digit, in: "):
        """Intialise."""
        self.message = message
        self.pos = pos
        super().__init__(self.message + POSITIONS[pos])


class MultipleAssignmentsError(Exception):
    """Raised when a name is defined to multiple devices."""

    def __init__(self, pos,
                 message="Syntax Error: One Name for Multiple Devices, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class ParameterLetterError(Exception):
    """Raised when a parameter is a Letter."""

    def __init__(self, pos,
                 message="Syntax Error: Parameter Cannot Be A Letter, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class UnexpectedEOFError(Exception):
    """Raised when an EOF is encountered."""

    def __init__(self, pos,
                 message="Syntax Error: Unexpected EOF encountered, in:"):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class InvalidSymbolError(Exception):
    """Raised when a symbol is invalid."""

    def __init__(self, pos,
                 message="Syntax Error: Symbol not valid :"):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class UnexpectedKeywordError(Exception):
    """Raised when a keyword is encountered."""

    def __init__(self, pos,
                 message="Syntax Error: Unexpected Keyword encountered, in:"):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class InvalidPunctError(Exception):
    """Raised when punctuation is invalid."""

    def __init__(self, pos,
                 message="Syntax Error: Punctuation not valid, in :"):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class SyntaxErrorsC():
    """Contains the different syntax errors as methods."""

    def __init__(self):
        """Intialise."""
        pass

    def CharNotSupported(pos, messageC=None):
        """Raise Error."""
        raise CharNotSupportedError(pos, messageC)

    def DigitStartsName(pos, messageC=None):
        """Raise Error."""
        raise DigitStartsNameError(pos, messageC)

    def MultipleAssignments(pos, messageC=None):
        """Raise Error."""
        raise MultipleAssignmentsError(pos, messageC)

    def ParameterLetter(pos, messageC=None):
        """Raise Error."""
        raise ParameterLetterError(pos, messageC)

    def UnexpectedEOF(pos, messageC=None):
        """Raise Error."""
        raise UnexpectedEOFError(pos, messageC)

    def InvalidSymbol(pos, messageC=None):
        """Raise Error."""
        raise InvalidSymbolError(pos, messageC)

    def UnexpectedKeyword(pos, messageC=None):
        """Raise Error."""
        raise UnexpectedKeywordError(pos, messageC)

    def InvalidPunct(pos, messageC=None):
        """Raise Error."""
        raise InvalidPunctError(pos, messageC)


# Semantic Errors
class InputNotAssignedError(Exception):
    """Raised when an input to a device is left unassigned."""

    def __init__(self, pos,
                 message="Semantic Error: Input to Device Unassigned, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class InputToSwitchAssignedError(Exception):
    """Raised when input to a switch is assigned."""

    def __init__(self, pos,
                 message="Semantic Error: Input to Switch Assigned, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])
# NOTE: CLOCK PERIOD CANNOT BE ZERO ERROR -> ValueError


class ReferencedBeforeAssignedError(Exception):
    """Raised when a component is referenced before it is assigned."""

    def __init__(self, pos,
                 message="Semantic Error: Referenced Before Assigned, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class AlreadyAssignedError(Exception):
    """Raised when a component has already been assigned."""

    def __init__(self, pos,
                 message="Semantic Error: Already Been Assigned, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class DeviceNameIError(Exception):
    """Raised when a device is named "I"."""

    def __init__(self, pos,
                 message="Semantic Error: Device Name Cannot Be 'I', in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class MonitorOnInputError(Exception):
    """Raised when a monitor is placed on an input."""

    def __init__(self, pos,
                 message="Semantic Error: Monitor Placed On An Input, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class DeviceNotExistError(Exception):
    """Raised when a device is called that does not exist."""

    def __init__(self, pos,
                 message="Semantic Error: Device Does Not Exist, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class PinNotExistError(Exception):
    """Raised when a pin is called that does not exist."""

    def __init__(self, pos,
                 message="Semantic Error: Input Pin Does Not Exist, in: "):
        """Intialise."""
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])


class SemanticErrorsC:
    """Contains the different Semantic Errors as methods."""

    def __init__(self):
        """Initialise."""
        pass

    def InputNotAssigned(pos, messageC=None):
        """Raise Error."""
        raise InputNotAssignedError(pos, messageC)

    def InputToSwitchAssigned(pos, messageC=None):
        """Raise Error."""
        raise InputNotAssignedError(pos, messageC)

    def ClockPeriodZero(pos, messageC=None):
        """Raise Error."""
        raise ValueError(messageC + POSITIONS[pos])

    def ReferencedBeforeAssigned(pos, messageC=None):
        """Raise Error."""
        raise ReferencedBeforeAssignedError(pos, messageC)

    def AlreadyAssigned(pos, messageC=None):
        """Raise Error."""
        raise AlreadyAssignedError(pos, messageC)

    def DeviceNameI(pos, messageC=None):
        """Raise Error."""
        raise DeviceNameIError(pos, messageC)

    def MonitorOnInput(pos, messageC=None):
        """Raise Error."""
        raise MonitorOnInputError(pos, messageC)

    def DeviceNotExist(pos, messageC=None):
        """Raise Error."""
        raise DeviceNotExistError(pos, messageC)

    def PinNotExist(pos, messageC=None):
        """Raise Error."""
        raise PinNotExistError(pos, messageC)
