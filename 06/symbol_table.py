
PRE_DICT = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4
}
STARTING_INDEX = 16


class SymbolTable:
    def __init__(self):
        self.__symbol_table = dict()

    def get_symbol(self):
        print(self.__symbol_table)

    def add_entry(self, symbol, address=None):
        if address is None:
            i = STARTING_INDEX
            while i in self.__symbol_table.values():
                i += 1
            address = i

            if(address == 16):
                print(self.__symbol_table)
        self.__symbol_table.update({symbol: address})

    def is_contain(self, symbol):
        if symbol in self.__symbol_table:
            return True
        return False

    def get_address(self, symbol):
        if self.is_contain(symbol):
            return self.__symbol_table.get(symbol)

    def load_predefined_symbol(self):
        for key in PRE_DICT.keys():
            self.add_entry(key, PRE_DICT[key])
