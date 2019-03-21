from sys import argv
from CodeWriter import CodeWriter
from Parser import Parser

input = argv[1]

f = open(filename) #TODO: take in dir
parser = Parser(f)
#
f.close()

output_file = open(output_filename, 'w')
codeWriter = CodeWriter(output_file)
#
codeWriter.Close()
