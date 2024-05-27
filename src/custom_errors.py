"""Define Custom Errors; Syntax and Semanic."""


POSITIONS = ["DEVICES", "CONNECTIONS", "MONITORS"]


class SyntaxErrorsC():
    """Contains the different syntax errors as methods."""

    def __init__(self):
        """Intialise."""
        pass

    def CharNotSupported(pos):
        """Raise Error."""
        print("Syntax Error: Character Not Supported, in "
              + POSITIONS[pos])

    def DigitStartsName(pos):
        """Raise Error."""
        print("Syntax Error: Name Cannot Start With A Digit, in "
              + POSITIONS[pos])

    def MultipleAssignments(pos):
        """Raise Error."""
        print("Syntax Error: One Name for Multiple Devices, in "
              + POSITIONS[pos])

    def InvalidParameter(pos):
        """Raise Error."""
        print("Syntax Error: Invalid Parameter Value, in "
              + POSITIONS[pos])

    def UnexpectedEOF(pos):
        """Raise Error."""
        print("Syntax Error: Unexpected EOF Encountered, in "
              + POSITIONS[pos])

    def InvalidSymbol(pos):
        """Raise Error."""
        print("Syntax Error: Invalid Symbol, in "
              + POSITIONS[pos])

    def UnexpectedKeyword(pos):
        """Raise Error."""
        print("Syntax Error: Unexpected Keyword encountered, in "
              + POSITIONS[pos])

    def InvalidPunct(pos):
        """Raise Error."""
        print("Syntax Error: Punctuation not valid, in "
              + POSITIONS[pos])


class SemanticErrorsC:
    """Contains the different Semantic Errors as methods."""

    def __init__(self):
        """Initialise."""
        pass

    def InputNotAssigned(pos):
        """Raise Error."""
        print("Semantic Error: Input to Device Unassigned, in "
              + POSITIONS[pos])

    def InputToSwitchAssigned(pos):
        """Raise Error."""
        print("Semantic Error: Input to Switch Assigned, in "
              + POSITIONS[pos])

    def ClockPeriodZero(pos):
        """Raise Error."""
        print("Clock Period Cannot be Zero, in "
              + POSITIONS[pos])

    def ReferencedBeforeAssigned(pos):
        """Raise Error."""
        print("Semantic Error: Referenced Before Assigned, in "
              + POSITIONS[pos])

    def AlreadyAssigned(pos):
        """Raise Error."""
        print("Semantic Error: Already Been Assigned, in "
              + POSITIONS[pos])

    def DeviceNameI(pos):
        """Raise Error."""
        print("Semantic Error: Device Name Cannot Be 'I', in "
              + POSITIONS[pos])

    def MonitorOnInput(pos):
        """Raise Error."""
        print("Semantic Error: Monitor Placed On An Input, in "
              + POSITIONS[pos])

    def DeviceNotExist(pos):
        """Raise Error."""
        print("Semantic Error: Device Does Not Exist, in "
              + POSITIONS[pos])

    def PinNotExist(pos):
        """Raise Error."""
        print("Semantic Error: Input Pin Does Not Exist, in "
              + POSITIONS[pos])

    def ParameterNotAllowed(pos):
        """Raise Error."""
        print("Semantic Error: Parameter Not Allowed, in "
              + POSITIONS[pos])
