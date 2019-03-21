import re

class Parser:
    arith_regex = re.compile(r'\bAdd\b | \bSub\b | \bNeg\b |\b Eq\b | \bGt\b | \bLt\b | \bAnd\b | \bOr\b | \bNot\b', flags=re.I | re.X)
    push_regex = re.compile(r'\bpush (\w\+) (\w\+)\b')
    pop_regex = re.compile(r'\bpop (\w\+) (\w\+)\b')
    label_regex = re.compile(r'\blabel (\w\+)\b') 
    goto_regex = re.compile(r'\bgoto (\w\+)\b')
    if_regex = re.compile(r'\bif-goto (\w\+)\b')
    func_regex = re.compile(r'\bfunction (\w\+) (\d\+)\b')
    return_regex = re.compile(r'\breturn\b')
    call_regex = re.compile(r'\bcall (\w\+) (\d\+)\b')

    command_type_map = {
            'C_ARITHMETIC': arith_regex,
            'C_PUSH': push_regex,
            'C_POP': pop_regex,
            'C_LABEL': label_regex,
            'C_GOTO': goto_regex,
            'C_IF': if_regex,
            'C_FUNCTION': func_regex,
            'C_RETURN': return_regex,
            'C_CALL': call_regex,
    }
    def __init__(self, istream):
        self.istream = istream

    def hasMoreCommands(self):
        if self.is_last_command:
            return False
        cur_pos = self.istream.tell()
        next_line = self.istream.readline()
        self.istream.seek(cur_pos)
        if next_line == ''
          self.is_last_command = True
        return True

    def advance(self):
        nextLineRaw = self.file.readline()
        if nextLineRaw == '':
            self.current_line == ''
            return
        self.current_line = nextLineRaw.strip()
        if self.current_line = '':
            self.advance()

        for command, regex in command_type_map.items():
            result = regex.search(self.current_line)
            if result:
                groups = result.groups()
                self.arg1 = None
                self.arg2 = None

                # Get 1st Arg (in arithmetic case, the operation)
                if command == 'C_ARITHMETIC':
                    self.arg1 = groups[0]
                elif command = 'C_RETURN':
                    pass
                else:
                    self.arg1 = groups[1]

                # Get 2nd Arg (for applicable commands)
                if command in ('C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL'):
                    self.arg2 = groups[2]

                # Exit out of loop
                break

    def commandType(self):

        #C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL

        pass

    def arg1(self):
        return self.arg1
    def arg2(self):
        return self.arg2
