class CodeWriter():
    """
    This class represents a CodeWriter for translating vm files into
    assembly files.

    @type output_stream: TextIOWrapper
    @param output_stream: Stream for writing into output file

    @type jump_flag: int
    @param jump_flag: parameter to distinct between jump operations in the assembly
    translation process

    @type segment_to_command: dict
    @param segment_to_command: Dict that translates the type of the function into the
    string it needs to be in the assembly code
    """
    output_stream = None
    jump_flag = 0   
    segment_to_command = {'local': 'LCL', 'argument': 'ARG', 'temp': 'R5',
                            'this': 'THIS', 'that': 'THAT'}

    def __init__(self, output_file):
        self.output_stream = open(output_file, 'w')

    def write_arithmetic(self, command_type):
        """
        This function translate arithmetic commands into assembly

        @type command_type: str
        @param command_type: the type of the arithmetic command to be
        tranlated

        @returns: Output assembly
        """
        output = []
        if command_type == 'add':
            output = self.command_template1('+')

        elif command_type == 'sub':
            output = self.command_template1('-')
        
        elif command_type == 'neg':
            output = self.command_template3('-')
        
        elif command_type == 'eq':
            output = self.command_template2('JNE')
            self.jump_flag += 1
    
        elif command_type == 'gt':
            output = self.command_template2('JGE')
            self.jump_flag +=1

        elif command_type == 'lt':
            output = self.command_template2('JLE')
            self.jump_flag +=1

        elif command_type == 'and':
            output = self.command_template1('&')
        
        elif command_type == 'or':
            output = self.command_template1('|')
        
        elif command_type == 'not':
            output = self.command_template3('!')

        for line in output:
            self.output_stream.write(f"{line}\n")

    def write_push_pop(self, type, segment, index):
        """
        This function translate push/pop commands into assembly

        @type type: str
        @param type: the type of the command (push/pop)

        @type segment: str
        @param segment: The segment part of the command

        @type index: str
        @param index: The index part of the line

        @returns: Output assembly
        """
        output = []
        
        if type == 'push' and segment == 'constant':
            output.append('@' + index)
            output.append('D=A')
            output.append('@SP')
            output.append('A=M')
            output.append('M=D')
            output.append('@SP')
            output.append('M=M+1')
            

        if type == 'pop' and (segment == 'local' or segment == 'argument' or segment == 'temp' or segment == 'this' or segment == 'that'):
            if segment == 'temp':
                output = self.pop_template1(segment, int(index) + 5)
            else:
                output = self.pop_template1(segment, index)

        if type == 'push' and (segment == 'local' or segment == 'argument' or segment == 'temp' or segment == 'this' or segment == 'that'):
            if segment == 'temp':
                output = self.push_template1(segment, int(index) + 5)
            else:
                output = self.push_template1(segment, index)

        if type == 'pop' and segment == 'pointer' and index == '0':
            output = self.pop_template2(index, 'THIS')

        if type == 'pop' and segment == 'pointer' and index == '1':
            output = self.pop_template2(index, 'THAT')
            
        if type == 'push' and segment == 'pointer' and index == '0':
            output = self.push_template2(index, 'THIS')
            
        if type == 'push' and segment == 'pointer' and index == '1':
            output = self.push_template2(index, 'THAT')

        if type == 'push' and  segment == 'static':
            output = self.push_template2(index, str(16+int(index)))

        if type == 'pop' and segment == 'static':
            output = self.pop_template2(index, str(16+int(index)))


        for line in output:
            self.output_stream.write(f"{line}\n")

    def command_template1(self, sign):
        
        """
        This function returns a format commonly used in
        the translation process

        @type sign: str
        @param sign: The sign to be inserted

        @returns: Output assembly
        """
        output = []
        output.append('@SP')
        output.append('AM=M-1')
        output.append('D=M')
        output.append('@SP')
        output.append('M=M-1')
        output.append('A=M')
        output.append('M=M'+ sign +'D')
        output.append('@SP')    
        output.append('M=M+1')
        return output
    
    def command_template2(self, sign):
        
        """
        This function returns a format commonly used in
        the translation process

        @type sign: str
        @param sign: The sign to be inserted

        @returns: Output assembly
        """
        output = []
        output.append('@SP')
        output.append('AM=M-1')
        output.append('D=M')
        output.append('@SP')
        output.append('AM=M-1')
        output.append('D=D-M')
        output.append('@FALSE_' + str(self.jump_flag)) 
        output.append('D;'+ str(sign) +'')
        output.append('@SP')
        output.append('A=M')
        output.append('M=-1')
        output.append('@CONTINUE_' + str(self.jump_flag))
        output.append('0;JMP')
        output.append('(FALSE_' + str(self.jump_flag) + ')')
        output.append('@SP')
        output.append('A=M')
        output.append('M=0')
        output.append('(CONTINUE_' + str(self.jump_flag) + ')')
        output.append('@SP')
        output.append('M=M+1')
        return output

    def command_template3(self, sign):
        
        """
        This function returns a format commonly used in
        the translation process

        @type sign: str
        @param sign: The sign to be inserted

        @returns: Output assembly
        """
        output = []
        output.append('@SP')
        output.append('M=M-1')
        output.append('A=M')
        output.append('M='+ sign +'M')
        output.append('@SP')
        output.append('M=M+1')
        return output

    def push_template1(self, segment, index):
        
        """
        This function returns a format commonly used in
        the translation process

        @type segment: str
        @param segment: The segment part of the vm command
        
        @type index: str
        @param index: The index part of the vm command

        @returns: Output assembly
        """
        output = []
        output.append('@' + self.segment_to_command[segment])
        output.append('D=M')
        output.append('@'+str(index))
        output.append('A=D+A')
        output.append('D=M')
        output.append('@SP')
        output.append('A=M')
        output.append('M=D')
        output.append('@SP')
        output.append('M=M+1')
        return output

    def push_template2(self, index, segment):
        
        """
        This function returns a format commonly used in
        the translation process

        @type segment: str
        @param segment: The segment part of the vm command
        
        @type index: str
        @param index: The index part of the vm command

        @returns: Output assembly
        """
        output = []
        output.append('@' + segment)
        output.append('D=M')
        output.append('@SP')
        output.append('A=M')
        output.append('M=D')
        output.append('@SP')
        output.append('M=M+1')
        return output

    def pop_template1(self, segment, index):
        
        """
        This function returns a format commonly used in
        the translation process

        @type segment: str
        @param segment: The segment part of the vm command
        
        @type index: str
        @param index: The index part of the vm command

        @returns: Output assembly
        """
        output = []
        output.append('@' + self.segment_to_command[segment])
        output.append('D=M')
        output.append('@'+str(index))
        output.append('D=A+D')
        output.append('@R13')
        output.append('M=D')
        output.append('@SP')
        output.append('AM=M-1')
        output.append('D=M')
        output.append('@R13')
        output.append('A=M')
        output.append('M=D')
        return output

    def pop_template2(self, index, segment):
        
        """
        This function returns a format commonly used in
        the translation process

        @type segment: str
        @param segment: The segment part of the vm command
        
        @type index: str
        @param index: The index part of the vm command

        @returns: Output assembly
        """
        output = []
        output.append('@SP')
        output.append('AM=M-1')
        output.append('D=M')
        output.append('@' + segment)
        output.append('M=D')
        return output

    

    def close(self):
        
        """
        This function closes the writing stream to the file.

        @returns: None
        """
        self.output_stream.close()