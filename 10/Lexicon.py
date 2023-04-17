from enum import Enum

class Lexicon(Enum):

    KEYWORDS = ("class", "constructor", "function", "method", "field", "static", "var", 
                        "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
                        "do", "if", "else", "while", "return")

    SYMBOLS = ("{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|",
                        "<", ">", "=", "~")

    INT_CONST = range(0, 32768)

    STR_CONST = "^\\S+$"

    IDENTIFIER = "^[A-Za-z_]+[A-Za-z_0-9]+$"