from parser import Parser
from code_translator import CodeTranslator
from symbol_table import SymbolTable
import time

class HackAssembler:
    def __init__(self, file_name):
        # opens an input file and process it
        # Constructs a symbol table and adds the predefined symbols to it
        self.__translated_code = []
        self.__parser = Parser(file_name)
        self.__symbol = SymbolTable()
        self.__symbol.load_predefined_symbol()

    def first_pass(self):
        # reads the program lines and add all symbols to symbol table
        # focuses on labels
        line_number = 0
        while self.__parser.has_more_lines():
            if self.__parser.instruction_type() == "L_INSTRUCTION":
                self.__symbol.add_entry(self.__parser.symbol(), line_number)
            if self.__parser.instruction_type() == "A_INSTRUCTION" or self.__parser.instruction_type() == "C_INSTRUCTION":
                line_number += 1
            self.__parser.advance()

    def second_pass(self):
        # translates a symbol to the symbol table
        with open('PongTrue.hack', 'r') as f:
            a = f.readlines()
            f.close()
        for i, item in enumerate(a):
            a[i] = item.strip()

        index = 0

        self.__parser.go_to_start()
        symbols = []
        while self.__parser.has_more_lines():
            symbols.append(self.__parser.get_current_line())
            if self.__parser.instruction_type() == "A_INSTRUCTION":
                symbol = self.__parser.symbol()
                if not symbol.isnumeric():
                    if not self.__symbol.is_contain(symbol):
                        self.__symbol.add_entry(symbol)
                    binary_num = CodeTranslator.get_binary_num(self.__symbol.get_address(symbol))
                else:
                    binary_num = CodeTranslator.get_binary_num(int(symbol))
                #print(binary_num)

                self.__translated_code.append(binary_num)
            if self.__parser.instruction_type() == "C_INSTRUCTION":
                binary_code = CodeTranslator.get_c_instruction_binary(self.__parser)
                self.__translated_code.append(binary_code)
            self.__parser.advance()
            index += 1
        
        #print(self.__symbol.get_symbol())
        return symbols

    def output_file(self, symbols):
        print(len(symbols))
        with open('PongTrue.hack', 'r') as f:
            a = f.readlines()
            f.close()
        for i, item in enumerate(a):
            a[i] = item.strip()
        print(len(a))
        index = -1
        line_index = -1
        para = 0
        final = []
        with open('prog.hack', 'w') as file:
            

            for line in self.__translated_code:
                index+=1
                line_index+=1
                while(symbols[line_index].startswith('(')):
                    para += 1
                    line_index+=1
                if(line != a[index]):
                    print(index + 1)
                    print("correct line:" + a[index])
                    print("incorrect line: "+line)
                    print("symbol:" + symbols[line_index]+ "\n")
                    
                    time.sleep(1)
                
                
                file.write("%s\n" % line)
        print(index)
        print(para)

if __name__ == '__main__':
    assembler = HackAssembler(
        "C:\\Users\\aviv1\\projects\\University\\nand\\nand2tetris\\nand2tetris\\projects\\06\\pong\\Pong.asm")
    assembler.first_pass()
    symbols = assembler.second_pass()
    assembler.output_file(symbols)