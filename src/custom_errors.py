"""
Define Custom Errors; Syntax and Semanitc
"""
POSITIONS = ["DEVICES","CONNECTIONS","MONITORS"]
#Syntax Errors
class CharNotSupportedError(Exception):
    """
    Syntax Error Raised when a character out of the grammar is encountered
    """
    def __init__(self, pos, message="Syntax Error: Character Not Supported, in: "):
        self.message = message
        self.pos = pos
        super().__init__(self.message + POSITIONS[pos])

class DigitStartsNameError(Exception):
    """
    Syntax Error Raised when a name is defined that starts with a digit
    """
    def __init__(self, pos, message="Syntax Error: Name Cannot Start With A Digit, in: "):
        self.message = message
        self.pos = pos
        super().__init__(self.message + POSITIONS[pos])
    
class MultipleAssignmentsError(Exception):
    """
    Syntax Error Raised when a name is defined to multiple devices
    """
    def __init__(self, pos, message="Syntax Error: Same Name Assigned To More Than One Device, in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

class ParameterLetterError(Exception):
    """
    Syntax Error Raised when a parameter is a Letter 
    """
    def __init__(self, pos, message="Syntax Error: Patameter Cannot Be A Letter, in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

class SyntaxErrorsC():
    """
    Class that contains the different syntax errors as methods    
    """
    def __init__(self):
        pass
    
    def CharNotSupported(pos, messageC = None):
        raise CharNotSupportedError(pos, messageC)  
    
    def DigitStartsName(pos, messageC = None):
        raise DigitStartsNameError(pos, messageC)
    
    def MultipleAssignments(pos, messageC = None):
        raise MultipleAssignmentsError(pos, messageC)
    
    def ParameterLetter(pos, messageC = None):
        raise ParameterLetterError(pos, messageC)


#Semantic Errors
class InputNotAssignedError(Exception):
    """
    Semantic Error Raised when an input to a device is left unassigned 
    """
    def __init__(self, pos, message="Semantic Error: Input to Device Left Unassigned, in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

class InputToSwitchAssignedError(Exception):
    """
    Semantic Error Raised when input to a switch is assigned 
    """
    def __init__(self, pos, message="Semantic Error: Input to Switch Assigned, in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

# NOTE: CLOCK PERIOD CANNOT BE ZERO ERROR -> ValueError

class ReferencedBeforeAssignedError(Exception):
    """
    Semantic Error Raised when a component is referenced before it is assigned 
    """
    def __init__(self, pos, message="Semantic Error: Component Referenced Before Assigned, in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

class AlreadyAssignedError(Exception):
    """
    Semantic Error Raised when a component has already been assigned 
    """
    def __init__(self, pos, message="Semantic Error: Component Has Already Been Assigned, in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

class DeviceNameIError(Exception):
    """
    Semantic Error Raised when a device is named "I" 
    """
    def __init__(self, pos, message="Semantic Error: Device Name Cannot Be 'I', in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

class MonitorOnInputError(Exception):
    """
    Semantic Error Raised when a monitor is placed on an input 
    """
    def __init__(self, pos, message="Semantic Error: Monitor Cannot Be Placed On An Input, in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

class DeviceNotExistError(Exception):
    """
    Semantic Error Raised when a device is called that does not exist 
    """
    def __init__(self, pos, message="Semantic Error: Device Does Not Exist, in: "):
        self.pos = pos
        self.message = message
        super().__init__(self.message + POSITIONS[pos])

class SemanticErrorsC:
    """
    Class that contains the different Semantic Errors as methods
    """
    def __init__(self):
        pass
    
    def InputNotAssigned(pos, messageC = None):
        raise InputNotAssignedError(pos, messageC)
    
    def InputToSwitchAssigned(pos, messageC = None):
        raise InputNotAssignedError(pos, messageC)
    
    def ClockPeriodZero(pos, messageC = None):
        raise ValueError(messageC + POSITIONS[pos])
    
    def ReferencedBeforeAssigned(pos, messageC = None):
        raise ReferencedBeforeAssignedError(pos, messageC)
    
    def AlreadyAssigned(pos, messageC = None):
        raise AlreadyAssignedError(pos, messageC)
    
    def DeviceNameI(pos, messageC = None):
        raise DeviceNameIError(pos, messageC)
    
    def MonitorOnInput(pos, messageC = None):
        raise MonitorOnInputError(pos, messageC)
    
    def DeviceNotExist(pos, messageC = None):
        raise DeviceNotExistError(pos, messageC)