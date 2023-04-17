import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from parser import Parser
from code_translator import CodeTranslator

def translate_instruction(parser):
    dest = parser.dest()
    bin_dest = CodeTranslator.dest(dest)
    comp = parser.comp()
    bin_comp = CodeTranslator.comp(comp)
    jump = parser.jump()
    bin_jump = CodeTranslator.jump(jump)
    if parser.is_a_bit_on():
        a = "1"
    else:
        a = "0"
    print(f"111{a}{bin_comp}{bin_dest}{bin_jump}")


if __name__ == '__main__':
    bla = Parser("/Users/ority/Desktop/Studies/Digital systems/nand2tetris/repo/DigitalSystems/06/max/Max.asm")
    while bla.has_more_lines():
        # print(f"The current instruction is: {bla.get_current_line()}")
        # print(f"The type of the instruction is: {bla.instruction_type()}")
        # if bla.instruction_type() == "A_INSTRUCTION" or bla.instruction_type() == "L_INSTRUCTION":
        #     print(f"The symbol of the instruction is: {bla.symbol()}")
        if bla.instruction_type() == "C_INSTRUCTION":
            print(f"DEST: {bla.dest()}\t|"
                  f" COMP: {bla.comp()}\t|"
                  f" JMP: {bla.jump()}")
            print(f"DEST BINARY: {CodeTranslator.dest(bla.dest())}\t| COMP BINARY: {CodeTranslator.comp(bla.comp())}\t| JMP BINARY: {CodeTranslator.jump(bla.jump())}")
            translate_instruction(bla)
        bla.advance()
        # print()
