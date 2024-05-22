"""
Define Custom Errors; Syntax and Semanitc
"""


class CharNotSupportedError(Exception):
    """
    Error Raised when a character out of the grammar is encountered
    """
    pass
class DigitStartsNameError(Exception):
    """
    Error Raised when a name is defined that starts with a digit
    """
    pass
class MultipleAssignmentsError(Exception):
    """
    Error Raised when a name is defined to mult
    """
    pass
