from enum import Enum


class CommandType(Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"
    PUSH = "push"
    POP = "pop"
    LABEL = "label"
    GOTO = "goto"
    IF = "if-goto"
    FUNCTION = "function"
    RETURN = "return"
    CALL = "call"

    def is_arithmetic(self):
        return self in (self.ADD, self.SUB, self.NEG, self.EQ, self.GT, self.LT, self.AND, self.OR, self.NOT)


class Segment(Enum):
    constant = None
    local = "LCL"
    argument = "ARG"
    this = "THIS"
    that = "THAT"
    pointer = 3
    temp = 5

    def is_symbol(self):
        return self == self.local or self == self.argument or self == self.this or self == self.that

    def is_number(self):
        return self == self.pointer or self == self.temp

    """
    static
    """
