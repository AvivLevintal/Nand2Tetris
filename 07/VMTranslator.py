from Parser import Parser
from CodeWriter import CodeWriter
from commands import Commands
import sys

class VMTranslator():
    """
    This class represents a VMTranslator

    @type parser: Parser
    @param parser: Parser class to read input file and skip empty lines

    @type codeWriter: CodeWriter
    @param codeWriter: Translates lines of vm files into asm
    """
    parser = None
    codeWriter = None

    def __init__(self):
        """
        VMTranslator constructor
        """
        self.parser = Parser(sys.argv[1])
        filename = sys.argv[1].split('\\')[-1].split('.')[0]
        self.codeWriter = CodeWriter(filename + '.asm')




def main():
    translator = VMTranslator()
    while translator.parser.has_more_lines():
        translator.parser.advance()
        if translator.parser.command_type() == Commands.C_ARITHMETIC:
            translator.codeWriter.write_arithmetic(translator.parser.curr_command)

        elif translator.parser.command_type() == Commands.C_PUSH or translator.parser.command_type() == Commands.C_POP:
            translator.codeWriter.write_push_pop(translator.parser.arg1(), translator.parser.segment(), translator.parser.arg2())

    translator.codeWriter.close()

if __name__ == '__main__':
    main()