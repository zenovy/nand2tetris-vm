from sys import argv
from CodeWriter import CodeWriter
from Parser import Parser

filename = argv[1]
output_filename = argv[2]

# Open files
f = open(filename)
output_file = open(output_filename + '.asm', 'w')

parser = Parser(f)
codeWriter = CodeWriter(output_file)

while parser.has_more_commands():
    parser.advance()
    command_type = parser.command_type()
    arg1 = parser.arg1
    arg2 = parser.arg2
    if command_type == 'C_PUSH' or command_type == 'C_POP':
        codeWriter.write_push_pop(command_type, arg1, arg2)
    elif command_type == 'C_ARITHMETIC':
        codeWriter.write_arithmetic(arg1)
    else:
        raise Exception("Command type '{0}' not implemented yet".format(command_type))

# Close files
f.close()
codeWriter.close()
