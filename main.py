from CodeWriter import CodeWriter
from Parser import parse_commands
from argparse import ArgumentParser
from contextlib import ExitStack
from typing import IO

# Get the filename from the "--filename" argument
arg_parser = ArgumentParser()
arg_parser.add_argument(
    "--input_filepath",
    help=f"Path of the .vm file to translate",
    required=True,
)
args = arg_parser.parse_args()
filepath = args.input_filepath


def run():
    with ExitStack() as exit_stack:
        filename = filepath.split("/")[-1:][0].rstrip(".vm")
        input_file: IO = exit_stack.enter_context(open(filepath))
        output_file: IO = exit_stack.enter_context(open(filepath.rstrip("vm") + "asm", "w"))
        code_writer = CodeWriter(filename, output_file)

        for command_type, arg1, arg2 in parse_commands(input_file):
            code_writer.write_command(command_type, arg1, arg2)


if __name__ == "__main__":
    run()
