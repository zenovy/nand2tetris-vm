from CodeWriter import CodeWriter
from Parser import parse_commands
from argparse import ArgumentParser
from contextlib import ExitStack
from typing import IO

# Get the filename from the "--filename" argument
arg_parser = ArgumentParser()
arg_parser.add_argument(
    "--input_file",
    help=f"Name of the .vm file to translate",
    required=True,
)
args = arg_parser.parse_args()
filename = args.input_file


def run():
    with ExitStack() as exit_stack:
        input_file: IO = exit_stack.enter_context(open(filename))
        output_file: IO = exit_stack.enter_context(open(filename.rstrip("vm") + "asm", "w"))
        code_writer = CodeWriter(output_file)

        for command_type, arg1, arg2 in parse_commands(input_file):
            code_writer.write_command(command_type, arg1, arg2)


if __name__ == "__main__":
    run()
