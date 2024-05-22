"""
Define Custom Errors; Syntax and Semanitc
"""

#Syntax Errors
class CharNotSupportedError(Exception):
    """
    Syntax Error Raised when a character out of the grammar is encountered
    """
    def __init__(self, message="Syntax Error: Character Not Supported"):
        self.message = message
        super().__init__(self.message)

class DigitStartsNameError(Exception):
    """
    Syntax Error Raised when a name is defined that starts with a digit
    """
    def __init__(self, message="Syntax Error: Name Cannot Start With A Digit"):
        self.message = message
        super().__init__(self.message)
    
class MultipleAssignmentsError(Exception):
    """
    Syntax Error Raised when a name is defined to multiple devices
    """
    def __init__(self, message="Syntax Error: Same Name Assigned To More Than One Device"):
        self.message = message
        super().__init__(self.message)

class ParameterLetterError(Exception):
    """
    Syntax Error Raised when a parameter is a Letter 
    """
    def __init__(self, message="Syntax Error: Patameter Cannot Be A Letter"):
        self.message = message
        super().__init__(self.message)

class CustomSyntaxErrors():
    """
    Class that contains the different syntax errors as methods    
    """
    def __init__(self):
        pass
    def CharNotSupported():
        raise CharNotSupportedError  
    def DigitStartsName():
        raise DigitStartsNameError  
    def MultipleAssignments():
        raise MultipleAssignmentsError  
    def ParameterLetter():
        raise ParameterLetterError


#Semantic Errors
class InputNotAssignedError(Exception):
    """
    Semantic Error Raised when an input to a device is left unassigned 
    """
    def __init__(self, message="Semantic Error: Input to Device Left Unassigned"):
        self.message = message
        super().__init__(self.message)

class InputToSwitchAssignedError(Exception):
    """
    Semantic Error Raised when input to a switch is assigned 
    """
    def __init__(self, message="Semantic Error: Input to Switch Assigned"):
        self.message = message
        super().__init__(self.message)

# NOTE: CLOCK PERIOD CANNOT BE ZERO ERROR -> ValueError

class ReferencedBeforeAssignedError(Exception):
    """
    Semantic Error Raised when a component is referenced before it is assigned 
    """
    def __init__(self, message="Semantic Error: Component Referenced Before Assigned"):
        self.message = message
        super().__init__(self.message)

class AlreadyAssignedError(Exception):
    """
    Semantic Error Raised when a component has already been assigned 
    """
    def __init__(self, message="Semantic Error: Component Has Already Been Assigned"):
        self.message = message
        super().__init__(self.message)

class DeviceNameIError(Exception):
    """
    Semantic Error Raised when a device is named "I" 
    """
    def __init__(self, message="Semantic Error: Device Name Cannot Be 'I' "):
        self.message = message
        super().__init__(self.message)

class MonitorOnInputError(Exception):
    """
    Semantic Error Raised when a monitor is placed on an input 
    """
    def __init__(self, message="Semantic Error: Monitor Cannot Be Placed On An Input"):
        self.message = message
        super().__init__(self.message)

class DeviceNotExistError(Exception):
    """
    Semantic Error Raised when a device is called that does not exist 
    """
    def __init__(self, message="Semantic Error: Device Does Not Exist"):
        self.message = message
        super().__init__(self.message)

class CustomSemanticErrors:
    """
    Class that contains the different Semantic Errors as methods
    """
    def __init__(self):
        pass
    def InputNotAssigned():
        raise InputNotAssignedError
    def InputToSwitchAssigned():
        raise InputNotAssignedError
    def ClockPeriodZero():
        raise ValueError("Clock Period Cannot Be Zero")
    def ReferencedBeforeAssigned():
        raise ReferencedBeforeAssignedError
    def AlreadyAssigned():
        raise AlreadyAssignedError
    def DeviceNameI():
        raise DeviceNameIError
    def MonitorOnInput():
        raise MonitorOnInputError
    def DeviceNotExist():
        raise DeviceNotExistError