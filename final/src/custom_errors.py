"""Define Custom Errors; Syntax and Semanic."""


POSITIONS = ["DEVICES", "CONNECTIONS", "MONITORS"]


class SyntaxErrorsC:
    """Contains the different syntax errors as methods."""

    def __init__(self):
        """Intialise."""
        pass

    @staticmethod
    def CharNotSupported(pos):
        """Raise Error."""
        print("Syntax Error: Character Not Supported, in "
              + POSITIONS[pos])

    @staticmethod
    def DigitStartsName(pos):
        """Raise Error."""
        print("Syntax Error: Name Cannot Start With A Digit, in "
              + POSITIONS[pos])

    @staticmethod
    def MultipleAssignments(pos):
        """Raise Error."""
        print("Syntax Error: One Name for Multiple Devices, in "
              + POSITIONS[pos])

    @staticmethod
    def InvalidParameter(pos):
        """Raise Error."""
        print("Syntax Error: Invalid Parameter Value, in "
              + POSITIONS[pos])

    @staticmethod
    def UnexpectedEOF(pos):
        """Raise Error."""
        print("Syntax Error: Unexpected EOF Encountered, in "
              + POSITIONS[pos])

    @staticmethod
    def InvalidSymbol(pos):
        """Raise Error."""
        print("Syntax Error: Invalid Symbol, in "
              + POSITIONS[pos])

    @staticmethod
    def UnexpectedKeyword(pos):
        """Raise Error."""
        print("Syntax Error: Unexpected Keyword encountered, in "
              + POSITIONS[pos])

    @staticmethod
    def InvalidPunct(pos):
        """Raise Error."""
        print("Syntax Error: Punctuation not valid, in "
              + POSITIONS[pos])


class SemanticErrorsC:
    """Contains the different Semantic Errors as methods."""

    def __init__(self):
        """Initialise."""
        pass

    @staticmethod
    def InputNotAssigned(pos):
        """Raise Error."""
        print("Semantic Error: Input to Device Left Unassigned, in "
              + POSITIONS[pos])

    @staticmethod
    def InputAssigned(pos):
        """Raise Error."""
        print("Semantic Error: Input Not Allowed, in "
              + POSITIONS[pos])

    @staticmethod
    def ClockPeriodZero(pos):
        """Raise Error."""
        print("Clock Period Cannot be Zero, in "
              + POSITIONS[pos])

    @staticmethod
    def ReferencedBeforeAssigned(pos):
        """Raise Error."""
        print("Semantic Error: Referenced Before Assigned, in "
              + POSITIONS[pos])

    @staticmethod
    def AlreadyAssigned(pos):
        """Raise Error."""
        print("Semantic Error: Already Been Assigned, in "
              + POSITIONS[pos])

    @staticmethod
    def DeviceNameI(pos):
        """Raise Error."""
        print("Semantic Error: Device Name Cannot Be 'I', in "
              + POSITIONS[pos])

    @staticmethod
    def MonitorOnInput(pos):
        """Raise Error."""
        print("Semantic Error: Monitor Placed On An Input, in "
              + POSITIONS[pos])

    @staticmethod
    def DeviceNotExist(pos):
        """Raise Error."""
        print("Semantic Error: Device Does Not Exist, in "
              + POSITIONS[pos])

    @staticmethod
    def PinNotExist(pos):
        """Raise Error."""
        print("Semantic Error: Input Pin Does Not Exist, in "
              + POSITIONS[pos])

    @staticmethod
    def ParameterNotAllowed(pos):
        """Raise Error."""
        print("Semantic Error: Parameter Not Allowed, in "
              + POSITIONS[pos])

    @staticmethod
    def MonitorNotExist(pos):
        """Raise Error."""
        print("Semantic Error: Monitor Does Not Exist, in "
              + POSITIONS[pos])
