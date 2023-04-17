from Parser import Parser
from CodeWriter import CodeWriter
from commands import Commands
import sys
import os

class VMTranslator():
    """
    Th)is class represents a VMTranslator

    @type parser: Parser
    @param parser: Parser class to read input file and skip empty lines

    @type codeWriter: CodeWriter
    @param codeWriter: Translates lines of vm files into asm
    """
    parser = None
    codeWriter = None
    files = []
    folder_flag = False

    def __init__(self):
        """
        VMTranslator constructor
        """
        if os.path.isfile(sys.argv[1]):    
            os.chdir(os.path.dirname(sys.argv[1]))
            self.parser = Parser(sys.argv[1])
            filename = sys.argv[1].split('\\')[-1].split('.')[0]
            self.codeWriter = CodeWriter(filename + '.asm')

        elif os.path.isdir(sys.argv[1]):
            self.folder_flag = True
            os.chdir(sys.argv[1])
            dir = os.listdir()
            self.files = filter(lambda file: '.vm' in file, dir)
            self.files = list(map(lambda file: os.getcwd() + '/' + file, self.files))
            self.parser = Parser(self.files[0])
            
            dir_name = os.path.basename(sys.argv[1])
            output_file_name = f"{sys.argv[1]}/{dir_name}.asm"
            self.codeWriter = CodeWriter(output_file_name)
        
    def translate_file(self):
        while self.parser.has_more_lines():
            self.parser.advance()
            if self.parser.command_type() == Commands.C_ARITHMETIC:
                self.codeWriter.write_arithmetic(self.parser.curr_command)

            elif self.parser.command_type() == Commands.C_PUSH or self.parser.command_type() == Commands.C_POP:
                self.codeWriter.write_push_pop(self.parser.arg1(), self.parser.segment(), self.parser.arg2())
            
            elif self.parser.command_type() == Commands.C_LABEL:
                self.codeWriter.write_label(self.parser.get_label())
            
            elif self.parser.command_type() == Commands.C_GOTO:
                self.codeWriter.write_goto(self.parser.get_label())
                
            elif self.parser.command_type() == Commands.C_IF:
                self.codeWriter.write_ifgoto(self.parser.get_label())

            elif self.parser.command_type() == Commands.C_CALL:
                self.codeWriter.write_call(self.parser.get_label(), self.parser.arg2())

            elif self.parser.command_type() == Commands.C_FUNCTION:
                self.codeWriter.write_function(self.parser.get_label(), self.parser.arg2())

            elif self.parser.command_type() == Commands.C_RETURN:
                self.codeWriter.write_return()

    """
    Continue to the next file
    """
    def reinit_translator(self, file):
        self.parser = Parser(file)
        self.codeWriter.set_filename(os.path.basename(file).split('.')[0])


def main():
    translator = VMTranslator()
    if translator.folder_flag:
        translator.codeWriter.add_bootstrap()

    translator.translate_file()
    for i,file in enumerate(translator.files):
        if i > 0:
            translator.reinit_translator(file)
            translator.translate_file()
    translator.codeWriter.close()


if __name__ == '__main__':
    main()