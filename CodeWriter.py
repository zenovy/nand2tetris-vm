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
                # Set segment[index] to D register
                '@{index}',
                'D=A',
                '@{segment}',
                'A=D+A',
                'D=M',
                # Set SP* = D
                '@SP',
                'A=M',
                'M=D',
                # Increment SP
                '@SP',
                'M=M+1',
            ])
        elif command = 'C_POP':
            # TODO: Later...
            self.__writelines__([
                # Set D = SP*
                '@SP',
                'D=M',
                # Set segment[index] = D
                '@{segment}',
                'D=A',

                ###
                # Set (segment + index) to D
                '@{index}',
                'D=A',
                '@{segment}',
                'D=D+A',
                #
                '@SP',
                'A=M',
                # A = SP*, D = segment + index
                # Set D -> A, A -> D


                # Decrement SP
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
