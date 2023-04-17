import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from types_of_instructions import TypesOfInstructions

COMMENT_SYMBOL = "//"
LEADING_SYMBOL_JUMP = ";"
LEADING_SYMBOL_COMP = "="


class Parser:
    def __init__(self, assembly_file_path):
        with open(assembly_file_path, "r") as opened_file:
            self.__file_content = opened_file.read().split("\n")
        self.__current_line_number = -1
        self.advance()

    def has_more_lines(self):
        total_number_of_lines = len(self.__file_content) - 1
        if self.__current_line_number < total_number_of_lines:
            return True
        return False

    def advance(self):
        # TODO: small refactor is needed
        if self.has_more_lines():
            current_line = self.get_current_line()
            if not current_line.startswith(COMMENT_SYMBOL) and not current_line == "":
                self.__current_line_number += 1

            while self.has_more_lines() and (current_line.startswith(COMMENT_SYMBOL) or current_line == ""):
                self.__current_line_number += 1
                current_line = self.get_current_line()

    def get_current_line(self):
        instruction_without_ws = self.__file_content[self.__current_line_number].replace(" ", "")
        if COMMENT_SYMBOL in instruction_without_ws:
            return instruction_without_ws.split(COMMENT_SYMBOL)[0]
        return instruction_without_ws

    def instruction_type(self):
        a_instruction_symbol = str(TypesOfInstructions.A_INSTRUCTION.value)
        l_instruction_symbol = str(TypesOfInstructions.L_INSTRUCTION.value)

        if self.get_current_line().startswith(a_instruction_symbol):
            return TypesOfInstructions.A_INSTRUCTION.name
        elif self.get_current_line().startswith(l_instruction_symbol):
            return TypesOfInstructions.L_INSTRUCTION.name
        else:
            return TypesOfInstructions.C_INSTRUCTION.name

    def symbol(self):
        if self.instruction_type() == TypesOfInstructions.A_INSTRUCTION.name:
            return self.get_current_line()[1:]
        elif self.instruction_type() == TypesOfInstructions.L_INSTRUCTION.name:
            return self.get_current_line()[1:-1]

    def comp(self):
        current_instruction = self.get_current_line()
        if self.instruction_type() == TypesOfInstructions.C_INSTRUCTION.name:
            if LEADING_SYMBOL_COMP in current_instruction:
                current_instruction = current_instruction.split(LEADING_SYMBOL_COMP)[1]

            if LEADING_SYMBOL_JUMP in current_instruction:
                current_instruction = current_instruction.split(LEADING_SYMBOL_JUMP)[0]

            return current_instruction

    def jump(self):
        current_instruction = self.get_current_line()
        if self.instruction_type() == TypesOfInstructions.C_INSTRUCTION.name:
            if LEADING_SYMBOL_JUMP in current_instruction:
                return current_instruction.split(LEADING_SYMBOL_JUMP)[1]

    def dest(self):
        current_instruction = self.get_current_line()
        if self.instruction_type() == TypesOfInstructions.C_INSTRUCTION.name:
            if LEADING_SYMBOL_COMP in current_instruction:
                return current_instruction.split(LEADING_SYMBOL_COMP)[0]

    def get_current_line_number(self):
        return self.__current_line_number

    def go_to_start(self):
        self.__current_line_number = -1
        self.advance()

    def is_a_bit_on(self):
        if self.comp():
            if "M" in self.comp().upper():
                return True
        # if self.dest():
        #     if "M" in self.dest().upper():
        #         return True
        return False