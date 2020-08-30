import re

arith_regex = re.compile(r'\b(add|sub|neg|eq|gt|lt|and|or|not)', flags=re.I)
push_regex = re.compile(r'\bpush(?:\s+(\w+))(?:\s+(\w+))')
pop_regex = re.compile(r'\bpop(?:\s+(\w+))(?:\s+(\w+))')
label_regex = re.compile(r'\blabel(?:\s+(\w+))')
goto_regex = re.compile(r'\bgoto(?:\s+(\w+))')
if_regex = re.compile(r'\bif-goto(?:\s+(\w+))')
func_regex = re.compile(r'\bfunction(?:\s+(\w+))(?:\s+(\d+))')
return_regex = re.compile(r'\breturn\b')
call_regex = re.compile(r'\bcall(?:\s+(\w+))(?:\s+(\d+))')
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


class Parser:
    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.arg1 = None
        self.arg2 = None
        self.current_line = None
        self.is_last_command = False

    def has_more_commands(self):
        if self.is_last_command:
            return False
        cur_pos = self.input_stream.tell()
        next_line = self.input_stream.readline()
        self.input_stream.seek(cur_pos)
        if next_line == '':
            self.is_last_command = True
        return True

    def advance(self):
        next_line_raw = self.input_stream.readline()
        if next_line_raw == '':
            self.is_last_command = True
            self.current_line == ''
            return
        self.current_line = next_line_raw.strip()
        if self.current_line == '':
            print('B')
            self.advance()

        for command, regex in command_type_map.items():
            result = regex.search(self.current_line)
            if result:
                print(self.current_line)
                self.command = command
                groups = result.groups()
                self.arg1 = None
                self.arg2 = None

                # Get 1st Arg (in arithmetic case, the operation)
                if command == 'C_RETURN':
                    if self.arg1:
                        raise Exception('Extra argument passed into return statement: `{}`'.format(self.current_line))
                else:
                    self.arg1 = groups[0]

                # Get 2nd Arg (for applicable commands)
                if command in ('C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL'):
                    self.arg2 = groups[1]
                elif self.arg2:
                    raise Exception('Extra argument passed into line `{}`'.format(self.current_line))

                # Exit out of loop
                break

    def command_type(self):
        return self.command

    def arg1(self):
        return self.arg1

    def arg2(self):
        return self.arg2
