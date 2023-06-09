from enum import Enum


class TypesOfComp(Enum):
    zero = "101010"
    one = "111111"
    minus_one = "111010"
    D = "001100"
    A = "110000"
    M = "110000"
    not_D = "001101"
    not_A = "110001"
    not_M = "110001"
    minus_D = "001111"
    minus_A = "110011"
    minus_M = "110011"
    D_plus_one = "011111"
    A_plus_one = "110111"
    M_plus_one = "110111"
    D_minus_one = "001110"
    A_minus_one = "110010"
    M_minus_one = "110010"
    D_plus_A = "000010"
    D_plus_M = "000010"
    D_minus_A = "010011"
    D_minus_M = "010011"
    A_minus_D = "000111"
    M_minus_D = "000111"
    D_and_A = "000000"
    D_and_M = "000000"
    D_or_A = "010101"
    D_or_M = "010101"