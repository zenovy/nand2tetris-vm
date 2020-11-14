from typing import IO, List

from VMTypes import CommandType


# Sets D to *y and A to &x
SET_BINARY_REGS = [
    "@0",
    "A=M-1",  # A = (SP)* - 1, or A = &y
    "D=M",   # D = *y
    "A=A-1",  # A = (SP)* - 2, or A = &x
]

# Sets A to &x
UNARY_SETUP = [
    "@0",
    "A=M-1",
]

# Sets SP* to SP* - 1
DECREMENT_SP = [
    "@0",
    "M=M-1",  # SP = SP - 1
]

CMD_TO_JMP_MAP = {
    CommandType.EQ: "JEQ",
    CommandType.LT: "JLT",
    CommandType.GT: "JGT",
}

"""
SEGMENT_TABLE = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
}
"""


class CodeWriter:
    def __init__(self, output_stream: IO):
        self.output_stream = output_stream
        self.count = 0
        """
        self._write_lines([
            # Initialize stack pointer
            "@256",
            "D=A",
            "@0",
            "A=D",
        ])
        """

    def _write_lines(self, lines: List[str]):
        for line in lines:
            self.output_stream.write(f"{line}\n")

    def write_arithmetic(self, command_type: CommandType):
        if command_type == CommandType.ADD:
            self._write_lines(
                SET_BINARY_REGS +
                ["M=D+M"] +
                DECREMENT_SP
            )
        elif command_type == CommandType.SUB:
            self._write_lines(
                SET_BINARY_REGS +
                ["M=M-D"] +
                DECREMENT_SP
            )
        elif command_type in (CommandType.EQ, CommandType.GT, CommandType.LT):
            jmp_label = self.count
            self.count += 1
            self._write_lines(
                SET_BINARY_REGS +
                [
                    "D=M-D",  # x - y
                    f"@CMP{jmp_label}TRUE",
                    f"D;{CMD_TO_JMP_MAP.get(command_type)}",
                    # False branch
                    "D=0",
                    f"@CMP{jmp_label}END",
                    "0;JMP",
                    # True branch
                    f"(CMP{jmp_label}TRUE)",
                    "D=-1",
                    # Finally branch
                    f"(CMP{jmp_label}END)",
                    "@0",
                    "A=M-1",
                    "A=A-1",
                    "M=D",
                ] + \
                DECREMENT_SP
            )
        elif command_type == CommandType.AND:
            self._write_lines(
                SET_BINARY_REGS +
                ["M=D&M"] +
                DECREMENT_SP
            )
        elif command_type == CommandType.OR:
            self._write_lines(
                SET_BINARY_REGS +
                ["M=D|M"] +
                DECREMENT_SP
            )
        elif command_type == CommandType.NEG:
            self._write_lines(
                UNARY_SETUP +
                ["M=-M"]
            )
        elif command_type == CommandType.NOT:
            self._write_lines(
                UNARY_SETUP +
                ["M=!M"]
            )
        else:
            raise RuntimeError(f"Command {command_type} not recognized")

    def write_push_pop(self, command: CommandType, segment: str, index):
        """
        if segment == "argument":
            pass
        if segment == "local":
            pass
        if segment == "this":
            pass
        if segment == "that":
            pass
        """
        if segment == "static":
            segment_start = 16
        elif segment == "constant":
            # If we set segment at 0, we can load constant with consecutive @{constant} and D=A
            segment_start = 0
        else:
            raise RuntimeError(f"Segment {segment} not implemented yet")
        if command == CommandType.PUSH:
            self._write_lines([
                # 1. Set D = segment[index]*
                "@{0}".format(segment_start + int(index)),
                "D=A" if segment == "constant" else "D=M",
                # 2. Set SP* = segment[index]*
                "@0",
                "A=M",  # Set SP address to A
                "M=D",  # Set value at SP to D
                # 3. Increment SP
                "@0",
                "M=M+1",
            ])
        elif command == CommandType.POP:
            self._write_lines([
                # 1. Set D = SP*
                "@0",
                "D=M",
                # 2. Set segment[index]* = D
                "@{0}".format(segment_start + index),
                "M=D",
                # 3. Decrement SP
                "@0",
                "M=M-1",
            ])
        else:
            raise RuntimeError("Command {} is not a valid command.".format(command))

    def write_command(self, command_type: CommandType, arg1: str, arg2: str):
        if command_type in (CommandType.PUSH, CommandType.POP):
            self.write_push_pop(command_type, arg1, arg2)
        elif command_type.is_arithmetic():
            self.write_arithmetic(command_type)
        else:
            raise RuntimeError(f"Command type '{command_type}' not implemented yet")
