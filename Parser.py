import re

from typing import IO, Tuple
from VMTypes import CommandType

command_type_regex_map = {
    CommandType.ADD: (re.compile(r"^(add)", flags=re.I)),
    CommandType.SUB: (re.compile(r"^(sub)", flags=re.I)),
    CommandType.NEG: (re.compile(r"^(neg)", flags=re.I)),
    CommandType.EQ: (re.compile(r"^(eq)", flags=re.I)),
    CommandType.GT: (re.compile(r"^(gt)", flags=re.I)),
    CommandType.LT: (re.compile(r"^(lt)", flags=re.I)),
    CommandType.AND: (re.compile(r"^(and)", flags=re.I)),
    CommandType.OR: (re.compile(r"^(or)", flags=re.I)),
    CommandType.NOT: (re.compile(r"^(not)", flags=re.I)),
    CommandType.PUSH: (re.compile(r"^push(?:\s+(\w+))(?:\s+(\w+))")),
    CommandType.POP: (re.compile(r"^pop(?:\s+(\w+))(?:\s+(\w+))")),
    CommandType.LABEL: (re.compile(r"^label(?:\s+(\w+))")),
    CommandType.GOTO: (re.compile(r"^goto(?:\s+(\w+))")),
    CommandType.IF: (re.compile(r"^if-goto(?:\s+(\w+))")),
    CommandType.FUNCTION: (re.compile(r"^function(?:\s+(\w+))(?:\s+(\d+))")),
    CommandType.RETURN: (re.compile(r"^return\b")),
    CommandType.CALL: (re.compile(r"^call(?:\s+(\w+))(?:\s+(\d+))")),
}


class ParsingError(RuntimeError):
    pass


def parse_commands(input_stream: IO) -> Tuple[CommandType, str, str]:
    for line in input_stream:
        if line == "":  # EOF
            return None
        for command_type, regex in command_type_regex_map.items():
            result = regex.search(line)
            if not result or line.strip() == "":
                continue  # Line can be ignored (e.g. a comment) or malformed line. TODO: detect input errors
            args = result.groups()  # Skip the first group, which is just the whole expression
            assert len(args) < 3
            print(f"{line}: {str(command_type)} + {','.join(args)} # {len(args)}")
            # arg1, arg2 = groups

            # Check that `return` command has no arguments
            if len(args) > 0 and command_type == CommandType.RETURN:
                raise ParsingError(f"Extra argument passed into return statement: `{line}`")

            # Check that unary commands have only one argument
            if len(args) > 1 and command_type not in (CommandType.PUSH, CommandType.POP, CommandType.FUNCTION, CommandType.CALL):
                raise ParsingError(f"Extra argument passed into line `{line}`")
            arg1 = result.group(1) if len(args) > 0 else None
            arg2 = result.group(2) if len(args) > 1 else None
            print(arg1, arg2)

            yield command_type, arg1, arg2
            break  # Exit out of inner loop for the next command
