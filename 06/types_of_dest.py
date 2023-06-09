from enum import Enum


class TypesOfDest(Enum):
    NONE = "000"
    M = "001"
    D = "010"
    DM = "011"
    MD = "011"
    A = "100"
    AM = "101"
    MA = "101"
    AD = "110"
    DA = "110"
    AMD = "111"
    DMA = "111"
    DAM = "111"
    MAD = "111"
    MDA = "111"
    ADM = "111"