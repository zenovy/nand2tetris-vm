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
