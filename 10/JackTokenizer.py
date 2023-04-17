
import re
from Lexicon import Lexicon

class JackTokenizer:
    """
    This class represents a JackTokenizer for tokenizing a file pre creating xml stage.
    """
    def __init__(self, filename):
        self.input_file = filename


    def _read_and_parse(self):
        """
        Function for reading a and parsing a file. Opens a stream to file,
        uses regex to remove any complicated comment blocks.

        @type return: list
        @returns: parsed list of the lines of the file, prepared for tokenizing process
        """
        regex_str = "/\\*+[^*]*\\*+(?:[^/*][^*]*\\*+)*/"
        multiline_flag = False
        parsed_list = []

        with open(self.input_file, mode="r") as f:
            lines = f.read().splitlines()

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                elif multiline_flag and "*/" not in line:
                    continue
                elif line.startswith("//"):
                    continue
                else:
                    if "//" in line:
                        line = line.split("//")[0]
                    
                    output_list = re.split(regex_str, line)
                    for output in output_list:
                        if output:
                            if "/*" in output or "/**" in output:
                                multiline_flag = True
                            elif "*/" in output:
                                multiline_flag = False
                            else:
                                parsed_list.append(output)
            f.close()
        
        return parsed_list

    def _generate_token_list(self, parsed_list):
        """
        Function for generating the token list of the file.

        @type parsed_list: list
        @param parsed_list: the lines of the file, without the comments.

        @type return: list
        @returns: tokenized list prepared for being written as XML file.
        """
        token_list = ["<tokens>"]

        for line in parsed_list:
            self._code_to_tokens(line, token_list)

        token_list.append("</tokens>")

        return token_list

    def _code_to_tokens(self, line, token_list):
        """
        Function for tokenizing a given line into XML token format.

        @type line: str
        @param line: the line to be tokenized.

        @type token_list: list
        @param token_list: list to appened the tokenized line.

        @returns: None
        """
        curr_code = ""
        str_tag = False

        for char in line:
            if char != " ":
                if char in Lexicon.SYMBOLS.value:
                    if curr_code in Lexicon.KEYWORDS.value:
                        token_list.append(self.format_token("keyword", curr_code))
                    elif curr_code.isdigit() and int(curr_code) in Lexicon.INT_CONST.value:
                        token_list.append(self.format_token("integerConstant", curr_code))
                    elif curr_code and curr_code[-1] == "\"" and not str_tag:
                        token_list.append(self.format_token("stringConstant", curr_code.split("\"")[1]))
                    elif curr_code:
                        token_list.append(self.format_token("identifier", curr_code))
                    curr_code = ""
                    if char == "<":
                        token_list.append(self.format_token("symbol", "&lt;"))
                    elif char == ">":
                        token_list.append(self.format_token("symbol", "&gt;"))
                    elif char == "&":
                        token_list.append(self.format_token("symbol", "&amp;"))
                    else:  
                        token_list.append(self.format_token("symbol", char))
                else:
                    if char == "\"":
                        if not str_tag:
                            str_tag = True
                        else:
                            str_tag = False
                    curr_code += char
            else:
                if curr_code in Lexicon.KEYWORDS.value:
                    token_list.append(self.format_token("keyword", curr_code))
                    curr_code = ""
                elif curr_code in Lexicon.SYMBOLS.value:
                    if curr_code == "<":
                        token_list.append(self.format_token("symbol", "&lt;"))
                    elif curr_code == ">":
                        token_list.append(self.format_token("symbol", "&gt;"))
                    elif char == "&":
                        token_list.append(self.format_token("symbol", "&amp;"))
                    else:  
                        token_list.append(self.format_token("symbol", curr_code))
                    curr_code = ""
                elif curr_code.isdigit() and int(curr_code) in Lexicon.INT_CONST.value:
                    token_list.append(self.format_token("integerConstant", curr_code))
                    curr_code = ""
                elif curr_code and curr_code[-1] == "\"" and not str_tag:
                    token_list.append(self.format_token("stringConstant", curr_code.split("\"")[1]))
                    curr_code = ""
                elif curr_code and str_tag:
                    curr_code += char
                elif curr_code:
                    token_list.append(self.format_token("identifier", curr_code))
                    curr_code = ""

    def format_token(self, keyword, value):
        """
        Function for formatting a token.

        @type keyword: str
        @param keyword: keyword of token.

        @type value: str
        @param value: value of token.

        @type return: str
        @returns: formatted token.
        """
        return ("<"+keyword+"> " + value + " </" + keyword + ">")

    def generate_tokens(self):
        """
        Public function for generating the token list of the file. For the use of the
        JackAnalyzer for generating XML.

        @type return: list
        @returns: tokenized list prepared for being written as XML file.
        """
        parsed_list = self._read_and_parse()
        
        token_list = self._generate_token_list(parsed_list)

        return token_list
