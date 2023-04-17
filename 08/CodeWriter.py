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
    segment_to_command = {'local': 'LCL', 'argument': 'ARG', 'pointer': 'R3', 'temp': 'R5',
                               'this': 'THIS', 'that': 'THAT'}
    return_flag = 0
    filename_static = '' 



    def __init__(self, output_file):
        self.output_stream = open(output_file, 'w')

    def set_filename(self, filename):
        self.filename_static = filename

    def write_arithmetic(self, command_type):
        """
        This function translate arithmetic commands into assembly

        @type command_type: str
        @param command_type: the type of the arithmetic command to be
        tranlated

        @returns: None
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
            output = self.command_template2('JLE')
            self.jump_flag +=1

        elif command_type == 'lt':
            output = self.command_template2('JGE')
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

        @returns: None
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
            
        elif type == 'pop' and (segment == 'pointer' or segment == 'temp'):
            output = self.pop_template1(self.segment_to_command[segment], index, True)
            
        elif type == 'push' and (segment == 'pointer' or segment == 'temp'):
            output = self.push_template1(self.segment_to_command[segment], index, True)

        elif type == 'push' and  segment == 'static':
            output = self.push_static(self.filename_static + str(index))

        elif type == 'pop' and segment == 'static':
            output = self.pop_static(self.filename_static + str(index))

        elif type == 'pop':
            output = self.pop_template1(self.segment_to_command[segment], index, False)
        else:
            output = self.push_template1(self.segment_to_command[segment], index, False)

        for line in output:
            self.output_stream.write(f"{line}\n")


    def write_label(self, label):
        """
        This function translate label commands into assembly

        @type label: str
        @param label: The label to be written in the assembly code
        @returns: None
        """

        self.output_stream.write(f"({label})\n")
    
    def write_goto(self, label):
        
        """
        This function translate goto commands into assembly

        @type label: str
        @param label: The label to be written in the assembly code
        @returns: Output assembly
        """
        self.output_stream.write(f"@{label}\n")
        self.output_stream.write(f"0;JMP\n")
        
    def write_ifgoto(self, label):
        
        """
        This function translate If commands into assembly

        @type label: str
        @param label: The label to be written in the assembly code
        @returns: Output assembly
        """
        output = []
        output = self.ifgoto_template(label)
        for line in output:
            self.output_stream.write(f"{line}\n")
    
    def write_call(self, function_name, nArgs):
        """
        This function translate call commands into assembly

        @type function_name: str
        @param function_name: The name of the called function

        @type nArgs: int
        @param nArgs: The number of arguments to be delivered to the called function

        @returns: None
        """
        output = []
        self.return_flag += 1
        output.append('@RETURN_' + str(self.return_flag))
        output.append('D=A')
        output.append('@SP')
        output.append('A=M')
        output.append('M=D')
        output.append('@SP')
        output.append('M=M+1')
        output = output + self.push_template1('LCL', 0, True)
        output = output + self.push_template1('ARG', 0, True)
        output = output + self.push_template1('THIS', 0, True)
        output = output + self.push_template1('THAT', 0, True)
        output.append('@SP')
        output.append('D=M')
        output.append('@5')
        output.append('D=D-A')
        output.append('@' + nArgs)
        output.append('D=D-A')
        output.append('@ARG')
        output.append('M=D')
        output.append('@SP')
        output.append('D=M')
        output.append('@LCL')
        output.append('M=D')
        output.append('@' + function_name)
        output.append('0;JMP')
        output.append('(RETURN_' + str(self.return_flag) + ')')

        for line in output:
            self.output_stream.write(f"{line}\n")

    def add_bootstrap(self):
        """
        Adds bootstrap to mulit file projects

        @returns: None
        """
        bootstrap = ['@256', 'D=A', '@SP', 'M=D']
        for line in bootstrap:
            self.output_stream.write(f"{line}\n")
        self.write_call('Sys.init', '0')

    def write_function(self, function_name, nVars):
        """
        This function translate call commands into assembly

        @type function_name: str
        @param function_name: The name of the called function

        @type nVars: int
        @param nVars: The number of arguments delivered to the called function

        @returns: None
        """
        self.write_label(function_name)
        for i in range(0, int(nVars)):
            self.write_push_pop('push', 'constant', '0')

    def write_return(self):
        """
        This function translate return commands into assembly

        @returns: None
        """
        output = []
        output.append("@LCL")
        output.append("D=M")
        output.append("@R11")
        output.append("M=D")
        output.append("@5")
        output.append("A=D-A")
        output.append("D=M")
        output.append("@R12")
        output.append("M=D")
        output = output + self.pop_template1(self.segment_to_command['argument'], 0, False)
        output.append("@ARG")
        output.append("D=M")
        output.append("@SP")
        output.append("M=D+1")
        output = output + self.return_template("THAT")
        output = output + self.return_template("THIS")
        output = output + self.return_template("ARG")
        output = output + self.return_template("LCL")
        output.append("@R12")
        output.append("A=M")
        output.append("0;JMP")
        for line in output:
            self.output_stream.write(f"{line}\n")

    def return_template(self, segement):
        """
        This function is a template used by the write return

        @returns: output
        """
        output = []
        output.append("@R11")
        output.append("D=M-1")
        output.append("AM=D")
        output.append("D=M")
        output.append("@" + segement)
        output.append("M=D")
        return output

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
        output.append('A=A-1')
        output.append('M=M'+ sign +'D')
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
        output.append('A=A-1')
        output.append('D=M-D')
        output.append('@FALSE_' + str(self.jump_flag)) 
        output.append('D;'+ str(sign) +'')
        output.append('@SP')
        output.append('A=M-1')
        output.append('M=-1')
        output.append('@CONTINUE_' + str(self.jump_flag))
        output.append('0;JMP')
        output.append('(FALSE_' + str(self.jump_flag) + ')')
        output.append('@SP')
        output.append('A=M-1')
        output.append('M=0')
        output.append('(CONTINUE_' + str(self.jump_flag) + ')')
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
        output.append('A=M-1')
        output.append('M='+ sign +'M')
        return output

    def push_template1(self, segment, index, isPointer):
        
        """
        This function returns a format commonly used in
        the translation process

        @type segment: str
        @param segment: The segment part of the vm command
        
        @type index: str
        @param index: The index part of the vm command

        @type isPointer: boolean
        @param isPointer: some of the push commands are of type pointer and needs
        to be treated accordingly

        @returns: Output assembly
        """
        output = []
        output.append('@' + str(index))
        output.append('D=A')
        output.append('@' + segment)
        if isPointer:
            output.append('A=A+D')
        else:
            output.append('A=M+D')
        output.append('D=M')
        output.append('@SP')
        output.append('A=M')
        output.append('M=D')
        output.append('@SP')
        output.append('M=M+1')
        return output

    def pop_template1(self, segment, index, isPointer):
        

        """
        This function returns a format commonly used in
        the translation process

        @type segment: str
        @param segment: The segment part of the vm command
        
        @type index: str
        @param index: The index part of the vm command

        @type isPointer: boolean
        @param isPointer: some of the push commands are of type pointer and needs
        to be treated accordingly

        @returns: Output assembly
        """        
        output = []
        output.append('@' + str(index))
        output.append('D=A')
        output.append('@' + segment)
        if isPointer:
            output.append('D=A+D')
        else:
            output.append('D=M+D')    
        output.append('@R13')
        output.append('M=D')
        output.append('@SP')
        output.append('AM=M-1')
        output.append('D=M')
        output.append('@R13')
        output.append('A=M')
        output.append('M=D')
        return output

    def push_static(self, segment):
        
        """
        This function returns a format commonly used in
        the translation process

        @type segment: str
        @param segment: The segment part of the vm command

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
    
    def pop_static(self, segment):
                
        """
        This function returns a format commonly used in
        the translation process

        @type segment: str
        @param segment: The segment part of the vm command

        @returns: Output assembly
        """
        output = []
        output.append('@SP')
        output.append('AM=M-1')
        output.append('D=M')
        output.append('@' + segment)
        output.append('M=D')
        return output

    def ifgoto_template(self, label):
                
        """
        This function returns a format commonly used in
        the translation process

        @type label: str
        @param label: The segment part of the vm command

        @returns: Output assembly
        """
        output = []
        output.append('@SP')
        output.append('AM=M-1')
        output.append('D=M')
        output.append('A=A-1')
        output.append('@' + label)
        output.append('D;JNE')
        return output


    def close(self):
        
        """
        This function closes the writing stream to the file.

        @returns: None
        """
        self.output_stream.close()