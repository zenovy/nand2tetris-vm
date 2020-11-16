from typing import IO, List

from VMTypes import CommandType, Segment


# Sets D to *y and A to &x
SET_BINARY_REGS = [
    "@SP",
    "A=M-1",  # A = (SP)* - 1, or A = &y
    "D=M",   # D = *y
    "A=A-1",  # A = (SP)* - 2, or A = &x
]

# Sets A to &x
UNARY_SETUP = [
    "@SP",
    "A=M-1",
]

# Sets SP* to SP* - 1
DECREMENT_SP = [
    "@SP",
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
    def __init__(self, filename: str, output_stream: IO):
        self.output_stream = output_stream
        self.filename = filename
        self.count = 0

    def _write_lines(self, lines: List[str]):
        for line in lines:
            self.output_stream.write(f"{line}\n")
            print(line)

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
                    "@SP",
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

    def _write_push(self, segment_name: str, index):
        index = int(index)
        segment = Segment[segment_name]
        segment_start = segment.value
        if segment == Segment.constant:
            self._write_lines([
                # Set D = index
                f"@{index}",
                "D=A",
            ])
        elif segment == Segment.static:
            self._write_lines([
                f"@{self.filename}.{index}",
                "D=M",
            ])
        elif segment.is_number():
            self._write_lines([
                f"@{segment_start + index}",
                "D=M",
            ])
        elif segment.is_symbol():
            self._write_lines([
                # Get value from segment
                f"@{index}",
                "D=A",
                f"@{segment_start}",
                "A=D+M",
                "D=M",
            ])
        else:
            raise RuntimeError(f"SegmentType {segment_name} is not a valid segment")
        self._write_lines([
            # Push D on top of stack and increment SP
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ])

    def _write_pop(self, segment_name: str, index):
        index = int(index)
        segment = Segment[segment_name]
        segment_start = segment.value
        if segment == Segment.constant:
            raise RuntimeError("Cannot pop into constant segment")
        elif segment == Segment.static:
            self._write_lines([
                f"@{self.filename}.{index}",
                "D=A",
            ])
        elif segment.is_number():
            # pointer and temp segments are in RAM[3-4] and RAM[5-12], respectively
            # TODO assert index (temp index < 8, pointer index < 2)
            self._write_lines([
                f"@{segment_start + index}",
                "D=A",
            ])
        elif segment.is_symbol():
            # local, argument, this, and that segments are pointers to that segment's base address
            self._write_lines([
                f"@{segment_start}",  # points to base
                "D=M",
                f"@{index}",
                "D=D+A",
            ])
        else:
            raise RuntimeError(f"SegmentType {segment_name} is not a valid segment")
        self._write_lines([
            # Store the destination address in register 15
            "@15",
            "M=D",
            # Decrement stack pointer and set D from top of stack
            "@SP",
            "M=M-1",
            "@SP",
            "A=M",
            "D=M",
            # Get destination address from register and load D
            "@15",
            "A=M",
            "M=D",
        ])

    def _write_label(self, label_name: str):
        self._write_lines([
            f"({label_name})",
        ])

    def _write_goto(self, dest: str):
        self._write_lines([
            f"@{dest}",
            "0;JMP",
        ])

    def _write_if_goto(self, dest: str):
        self._write_lines([
            "@SP",
            "M=M-1",
            "@SP",
            "A=M",
            "D=M",
            f"@{dest}",
            "D;JNE",
        ])

    def write_command(self, command_type: CommandType, arg1: str, arg2: str):
        if command_type.is_arithmetic():
            self.write_arithmetic(command_type)
        elif command_type == CommandType.PUSH:
            self._write_push(arg1, arg2)
        elif command_type == CommandType.POP:
            self._write_pop(arg1, arg2)
        elif command_type == CommandType.LABEL:
            self._write_label(arg1)
        elif command_type == CommandType.GOTO:
            self._write_goto(arg1)
        elif command_type == CommandType.IF_GOTO:
            self._write_if_goto(arg1)
        else:
            raise RuntimeError(f"Command type '{command_type}' not implemented yet")
