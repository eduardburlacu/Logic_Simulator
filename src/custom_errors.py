"""Define Custom Errors; Syntax and Semanic."""

POSITIONS = ["DEVICES", "CONNECTIONS", "MONITORS"]

class SyntaxErrorsC():
    """Contains the different syntax errors as methods."""

    def __init__(self):
        """Intialise."""
        pass

    def CharNotSupported(pos):
        """raise Error."""
        print("Syntax Error: Character Not Supported, in "
               + POSITIONS[pos])

    def DigitStartsName(pos):
        """raise Error."""
        print("Syntax Error: Name Cannot Start With A Digit, in "
               + POSITIONS[pos])

    def MultipleAssignments(pos):
        """raise Error."""
        print("Syntax Error: One Name for Multiple Devices, in "
               + POSITIONS[pos])

    def ParameterLetter(pos):
        """raise Error."""
        print("Syntax Error: Parameter Cannot Be A Letter, in "
               + POSITIONS[pos])

    def UnexpectedEOF(pos):
        """raise Error."""
        print("Syntax Error: Unexpected EOF encountered, in "
               + POSITIONS[pos])

    def InvalidSymbol(pos):
        """raise Error."""
        print("Syntax Error: Symbol not valid, in "
               + POSITIONS[pos])

    def UnexpectedKeyword(pos):
        """raise Error."""
        print("Syntax Error: Unexpected Keyword encountered, in "
               + POSITIONS[pos])

    def InvalidPunct(pos):
        """raise Error."""
        print("Syntax Error: Punctuation not valid, in "
               + POSITIONS[pos])


class SemanticErrorsC:
    """Contains the different Semantic Errors as methods."""

    def __init__(self):
        """Initialise."""
        pass

    def InputNotAssigned(pos):
        """raise Error."""
        print("Semantic Error: Input to Device Unassigned, in "
               + POSITIONS[pos])

    def InputToSwitchAssigned(pos):
        """raise Error."""
        print("Semantic Error: Input to Switch Assigned, in "
               + POSITIONS[pos])

    def ClockPeriodZero(pos):
        """raise Error."""
        print("Clock Period Cannot be Zero, in "
               + POSITIONS[pos])

    def ReferencedBeforeAssigned(pos):
        """raise Error."""
        print("Semantic Error: Referenced Before Assigned, in "
               + POSITIONS[pos])

    def AlreadyAssigned(pos):
        """raise Error."""
        print("Semantic Error: Already Been Assigned, in "
               + POSITIONS[pos])

    def DeviceNameI(pos):
        """raise Error."""
        print("Semantic Error: Device Name Cannot Be 'I', in "
               + POSITIONS[pos])

    def MonitorOnInput(pos):
        """raise Error."""
        print("Semantic Error: Monitor Placed On An Input, in "
               + POSITIONS[pos])

    def DeviceNotExist(pos):
        """raise Error."""
        print("Semantic Error: Device Does Not Exist, in "
               + POSITIONS[pos])

    def PinNotExist(pos, messageC=None):
        """raise Error."""
        print("Semantic Error: Input Pin Does Not Exist, in "
               + POSITIONS[pos])
