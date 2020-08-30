# Sets D to *y and A to &x
SET_BINARY_REGS = [
    '@SP',
    'A=M-1', # A = (SP)* - 1, or A = &y
    'D=M',   # D = *y
    'A=A-1', # A = (SP)* - 2, or A = &x
]

# Sets A to &x
UNARY_SETUP = [
    '@SP',
    'A=M-1',
]

# Sets SP* to SP* - 1
DECREMENT_SP = [
    '@SP',
    'M=M-1', # SP = SP - 1
]

CMD_TO_JMP_MAP = {
    'eq': 'JEQ',
    'lt': 'JLT',
    'gt': 'JGT',
}

'''
SEGMENT_TABLE = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
}
'''


class CodeWriter:
    def __init__(self, output_stream):
        self.output_stream = output_stream
        self.count = 0
        '''
        self._write_lines([
            # Initialize stack pointer
            '@256',
            'D=A',
            '@SP',
            'A=D',
        ])
        '''

    def set_file_name(self, filename):
        pass

    def write_arithmetic(self, command):
        if command == 'add':
            self._write_lines(
                SET_BINARY_REGS +
                ['M=D+M'] +
                DECREMENT_SP
            )
        elif command == 'sub':
            self._write_lines(
                SET_BINARY_REGS +
                ['M=M-D'] +
                DECREMENT_SP
            )
        elif command == 'eq' or command == 'gt' or command == 'lt':
            jmp_label = self.count
            self.count += 1
            self._write_lines(
                SET_BINARY_REGS +
                [
                    'D=M-D', # x - y
                    '@CMP{0}TRUE'.format(jmp_label),
                    'D;{0}'.format(CMD_TO_JMP_MAP.get(command)),
                    # FALSE
                    'D=0',
                    '@CMP{0}END'.format(jmp_label),
                    '0;JMP',
                    # TRUE
                    '(CMP{0}TRUE)'.format(jmp_label),
                    'D=-1',
                    # FINALLY
                    '(CMP{0}END)'.format(jmp_label),
                    '@SP',
                    'A=M-1',
                    'A=A-1',
                    'M=D',
                ] + \
                DECREMENT_SP
            )
        elif command == 'and':
            self._write_lines(
                SET_BINARY_REGS +
                ['M=D&M'] +
                DECREMENT_SP
            )
        elif command == 'or':
            self._write_lines(
                SET_BINARY_REGS +
                ['M=D|M'] +
                DECREMENT_SP
            )
        elif command == 'neg':
            self._write_lines(
                UNARY_SETUP +
                ['M=-M']
            )
        elif command == 'not':
            self._write_lines(
                UNARY_SETUP +
                ['M=!M']
            )
        else:
            raise Exception('Command {0} not recognized'.format(command))

    def write_push_pop(self, command, segment, index):
        if segment == 'constant':
            segment_start = 0
        if command == 'C_PUSH':
            self._write_lines([
                # 1. Set D = segment[index]*
                '@{0}'.format(segment_start + int(index)),
                'D=A' if segment == 'constant' else 'D=M',
                # 2. Set SP* = segment[index]*
                '@SP',
                'A=M', # Set SP address to A
                'M=D', # Set value at SP to D
                # 3. Increment SP
                '@SP',
                'M=M+1',
            ])
        elif command == 'C_POP':
            self._write_lines([
                # 1. Set D = SP*
                '@SP',
                'D=M',
                # 2. Set segment[index]* = D
                '@{0}'.format(segment_start + index),
                'M=D',
                # 3. Decrement SP
                '@SP',
                'M=M-1',
            ])
        else:
            raise Exception('Command {} is not a valid command.'.format(command))

    def close(self):
        self.output_stream.close()

    def _write_lines(self, lines):
        for line in lines:
            self.output_stream.write(line)
            self.output_stream.write('\n')
