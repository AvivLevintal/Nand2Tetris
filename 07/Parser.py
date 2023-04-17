from commands import Commands

class Parser():
    """
    This class represents a Parser for reading input vm file

    @type file_lines: List
    @param file_lines: The lines of the input file

    @type line_index: int
    @param line_index: current line

    @type curr_command: str
    @param curr_command: The current command read by the parser
    
    @type arithmetic_commands: List
    @param arithmetic_commands: List contains all aritmetic commands possible to parse
    """
    file_lines = []
    line_index =  0
    curr_command = ''
    arithmetic_commands = ['add', 'sub', 'neg',
                            'eq', 'gt', 'lt'
                            ,'and', 'or', 'not']

    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            self.file_lines = f.readlines()
            f.close()

    def has_more_lines(self):
        """
        Checks if the file has more lines to read
        @returns: boolean
        """
        return self.line_index < len(self.file_lines)

    def advance(self):
        """
        Advances to the next line, if there is one. Updateds the curr_command
        accordingly.
        @returns: None
        """
        while self.has_more_lines():
            current_line = self.file_lines[self.line_index]
            self.line_index += 1
            if current_line.startswith('//') or current_line == '\n':
                continue
            else: 
                self.curr_command = current_line.strip()
                break

            
    def command_type(self):
        """
        Returns the type of the command
        @returns: str
        """
        if self.curr_command in self.arithmetic_commands:
            return Commands.C_ARITHMETIC       
        elif 'push' in self.curr_command:
            return Commands.C_PUSH
        elif 'pop' in self.curr_command:
            return Commands.C_POP

    def arg1(self):
        """
        Returns the first argument of the line if the command is
        not return
        @returns: str
        """
        if(self.command_type() != Commands.C_RETURN):
            return self.curr_command.split(' ')[0]

    def arg2(self):
        """
        Returns the second argument of the line if the command is
        push, pop, call or function.
        @returns: str
        """
        if(self.command_type() == Commands.C_PUSH or
           self.command_type() == Commands.C_POP or
           self.command_type() == Commands.C_CALL or
           self.command_type() == Commands.C_FUNCTION):

           return self.curr_command.split(' ')[-1]
    
    def segment(self):
        """
        Returns the segment of the line if the command is
        push or pop.
        @returns: str
        """
        if(self.command_type() == Commands.C_POP or
           self.command_type() == Commands.C_PUSH):
            if('this' in self.curr_command):
                return 'this'
            elif('that' in self.curr_command):
                return 'that'
            elif('local' in self.curr_command):
                return 'local'
            elif('argument' in self.curr_command):
                return 'argument'
            elif('static' in self.curr_command):
                return 'static'
            elif('constant' in self.curr_command):
                return 'constant'
            elif('pointer' in self.curr_command):
                return 'pointer'
            elif('temp' in self.curr_command):
                return 'temp'