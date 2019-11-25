class CodeWriter:
    def __init__(self, ostream):
        self.ostream = ostream
    def setFileName(self, filename):
        pass
    def writeArithmetic(self, command):
        if command == 'add'
        self.ostream.write('@{}'.format(stack_begin + offset))
        pass
    def WritePushPop(self, command, segment, index):
        if command = 'C_PUSH':
            self.__writelines__([
                # 1. Set D = segment[index]*
                '@{0}'.format(segment + index},
                'D=M',
                # 2. Set SP* = segment[index]*
                '@SP',
                'A=M', # Set SP address to A
                'M=D', # Set value at SP to D
                # 3. Increment SP
                '@SP',
                'M=M+1',
            ])
        elif command = 'C_POP':
            self.__writelines__([
                # 1. Set D = SP*
                '@SP',
                'D=M',
                # 2. Set segment[index]* = D
                '@{0}'.format(segment + index},
                'M=D',
                # 3. Decrement SP
                '@SP',
                'M=M-1',
            ])
        else:
            raise Exception('Command {} is not a valid command.'.format(command))
    def Close(self):
        self.ostream.close()
    def __writelines__(self, lines):
        for line in lines:
            self.ostream.write(line)
            self.ostream.write('\n')
