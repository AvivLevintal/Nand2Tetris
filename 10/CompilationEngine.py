
class CompilationEngine:
    """
    Class that reads the tokenized XML, and convertes it to
    the final XML.
    """

    token_index = 0

    def __init__(self, filename):
        self.filename = filename

    def _read_and_parse_t(self):
        """
        Function for reading and parsing the lines of the T.XML

        @returns: None
        """
        token_list = []

        with open(self.filename, mode="r") as f:
            lines = f.read().splitlines()[1:-1]

            for line in lines:
                token_list.append(line)

        return token_list
                
    def _parse_tokens(self, token_list):
        """
        Function for processing a given token list into the final version list.

        @type token_list: list
        @param token_list: list to be procceced

        @returns: None
        """

        def _add_identation(ident_space, token):
            """
            Function for adding identation for the XML tree logic.

            @type ident_space: int
            @param ident_space: space units to be added

            @type token: str
            @param token: token to be idented.

            @type return: str
            @returns: idented token
            """
            return (" " * ident_space + token)

        def appnd_to_list(ident_space):
            """
            Function for adding token to final list.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            if self.token_index < len(token_list):
                final_list.append(_add_identation(ident_space, token_list[self.token_index]))
                self.token_index += 1

        def get_value(value):
            """
            Function for getting the value of the token.

            @type value: str
            @param value: value to be procecced
            
            @type return: str
            @returns: formatted value
            """
            return value.split(" ")[1]

        def compile_class(ident_space):
            """
            Function for compiling class token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            final_list.append(_add_identation(ident_space,"<class>"))

            for i in range(0 , 3):
                appnd_to_list(ident_space)
        
            while self.token_index < len(token_list) and ("static" in get_value(token_list[self.token_index]) or "field" in get_value(token_list[self.token_index])):
                compile_class_var_dec(ident_space + 2)
            
            while self.token_index < len(token_list) and ("constructor" in get_value(token_list[self.token_index]) or 
                    "function" in get_value(token_list[self.token_index]) or "method" in get_value(token_list[self.token_index])):
                compile_subroutine(ident_space + 2)

            appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</class>"))


        def compile_class_var_dec(ident_space):
            """
            Function for compiling class var dec token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            final_list.append(_add_identation(ident_space,"<classVarDec>"))

            appnd_to_list(ident_space)

            while self.token_index < len(token_list) and ";" not in get_value(token_list[self.token_index]):
                appnd_to_list(ident_space)

            appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</classVarDec>"))

        def compile_subroutine(ident_space):
            """
            Function for compiling subroutine token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            final_list.append(_add_identation(ident_space,"<subroutineDec>"))
            
            for i in range(0 , 4):
                appnd_to_list(ident_space)
            
            compile_parameter_list(ident_space + 2)

            appnd_to_list(ident_space)

            compile_subroutine_body(ident_space + 2)

            final_list.append(_add_identation(ident_space,"</subroutineDec>"))
        

        def compile_subroutine_body(ident_space):
            """
            Function for compiling subroutine body token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """            

            final_list.append(_add_identation(ident_space,"<subroutineBody>"))

            appnd_to_list(ident_space)

            while self.token_index < len(token_list) and ("let" not in get_value(token_list[self.token_index]) and 
                    "if" not in get_value(token_list[self.token_index]) and 
                    "while" not in get_value(token_list[self.token_index]) and 
                    "do" not in get_value(token_list[self.token_index]) and 
                    "return" not in get_value(token_list[self.token_index])):
                compile_var_dec(ident_space + 2)

            if self.token_index < len(token_list) and ("let" in get_value(token_list[self.token_index]) or 
                    "if" in get_value(token_list[self.token_index]) or 
                    "while" in get_value(token_list[self.token_index]) or 
                    "do" in get_value(token_list[self.token_index]) or 
                    "return" in get_value(token_list[self.token_index])):
                compile_statements(ident_space + 2)

            appnd_to_list(ident_space)
            final_list.append(_add_identation(ident_space,"</subroutineBody>"))


        def compile_parameter_list(ident_space):
            """
            Function for compiling parameter list token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """     

            final_list.append(_add_identation(ident_space,"<parameterList>"))

            while self.token_index < len(token_list) and ")" not in get_value(token_list[self.token_index]):

                for i in range(0 , 2):
                    appnd_to_list(ident_space)

                if self.token_index < len(token_list) and "," in get_value(token_list[self.token_index]):
                    appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</parameterList>"))

        def compile_var_dec(ident_space):
            """
            Function for compiling var dec token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """        
            
            final_list.append(_add_identation(ident_space,"<varDec>"))

            for i in range(0 , 3):
                appnd_to_list(ident_space)

            while self.token_index < len(token_list) and ";" not in get_value(token_list[self.token_index]):

                for i in range(0 , 2):
                    appnd_to_list(ident_space)

            appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</varDec>"))
        

        def compile_statements(ident_space):
            """
            Function for compiling statements token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            final_list.append(_add_identation(ident_space,"<statements>"))

            while self.token_index < len(token_list) and "}" not in get_value(token_list[self.token_index]):
                if self.token_index < len(token_list) and "let" in get_value(token_list[self.token_index]):
                    compile_let(ident_space + 2)
                elif self.token_index < len(token_list) and "if" in get_value(token_list[self.token_index]):
                    compile_if(ident_space + 2)
                elif self.token_index < len(token_list) and "while" in get_value(token_list[self.token_index]):
                    compile_while(ident_space + 2)
                elif self.token_index < len(token_list) and "do" in get_value(token_list[self.token_index]):
                    compile_do(ident_space + 2)
                elif self.token_index < len(token_list) and "return" in get_value(token_list[self.token_index]): 
                    compile_return(ident_space + 2)
            
            final_list.append(_add_identation(ident_space,"</statements>"))

        def compile_do(ident_space):
            """
            Function for compiling do token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            
            final_list.append(_add_identation(ident_space,"<doStatement>"))

            appnd_to_list(ident_space)

            compile_subroutine_call(ident_space)          

            appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</doStatement>"))

        def compile_subroutine_call(ident_space):
            
            """
            Function for compiling subroutine call token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            if self.token_index + 1< len(token_list) and "." in get_value(token_list[self.token_index + 1]):
                for i in range(0 , 2):
                    appnd_to_list(ident_space)
            
            for i in range(0 , 2):
                appnd_to_list(ident_space)
            compile_expression_list(ident_space + 2)
            appnd_to_list(ident_space)


        def compile_let(ident_space):
            """
            Function for compiling let token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            
            final_list.append(_add_identation(ident_space,"<letStatement>"))

            for i in range(0 , 2):
                appnd_to_list(ident_space)

            if self.token_index < len(token_list) and "[" in get_value(token_list[self.token_index]):
                appnd_to_list(ident_space)
                compile_expression(ident_space + 2)
                appnd_to_list(ident_space)
            
            appnd_to_list(ident_space)

            compile_expression(ident_space + 2)

            appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</letStatement>"))


        def compile_while(ident_space):
            """
            Function for compiling while token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            final_list.append(_add_identation(ident_space,"<whileStatement>"))

            for i in range(0 , 2):
                appnd_to_list(ident_space)

            compile_expression(ident_space + 2)

            for i in range(0 , 2):
                appnd_to_list(ident_space)
            
            compile_statements(ident_space + 2)
            
            appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</whileStatement>"))

        def compile_return(ident_space):
            
            """
            Function for compiling return token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            final_list.append(_add_identation(ident_space,"<returnStatement>"))

            appnd_to_list(ident_space)

            if self.token_index < len(token_list) and ";" not in get_value(token_list[self.token_index]):
                compile_expression(ident_space + 2)
            
            appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</returnStatement>"))


        def compile_if(ident_space):
            """
            Function for compiling if token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """    
            
            final_list.append(_add_identation(ident_space,"<ifStatement>"))

            for i in range(0 , 2):
                appnd_to_list(ident_space)
            compile_expression(ident_space + 2)
            
            for i in range(0 , 2):
                appnd_to_list(ident_space)
            
            compile_statements(ident_space + 2)
            
            appnd_to_list(ident_space)

            if self.token_index < len(token_list) and "else" in get_value(token_list[self.token_index]):

                for i in range(0 , 2):
                    appnd_to_list(ident_space)
                compile_statements(ident_space + 2)
                appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</ifStatement>"))
            

        def compile_expression(ident_space):
            
            """
            Function for compiling expressiong token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            final_list.append(_add_identation(ident_space,"<expression>"))

            compile_term(ident_space + 2)

            while self.token_index < len(token_list) and ("+" in get_value(token_list[self.token_index]) or 
                    "-" in get_value(token_list[self.token_index]) or 
                    "*" in get_value(token_list[self.token_index]) or 
                    "/" in get_value(token_list[self.token_index]) or 
                    "&amp;" in get_value(token_list[self.token_index]) or 
                    "|" in get_value(token_list[self.token_index]) or 
                    "&lt;" in get_value(token_list[self.token_index]) or 
                    "&gt;" in get_value(token_list[self.token_index]) or 
                    "=" in get_value(token_list[self.token_index])):
                appnd_to_list(ident_space)
                compile_term(ident_space + 2)

            final_list.append(_add_identation(ident_space,"</expression>"))


        def compile_term(ident_space):
            """
            Function for compiling term token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            
            final_list.append(_add_identation(ident_space,"<term>"))

            if self.token_index + 1< len(token_list) and "[" in get_value(token_list[self.token_index + 1]):
                for i in range(0 , 2):
                    appnd_to_list(ident_space)
                compile_expression(ident_space + 2)
                appnd_to_list(ident_space)
            elif self.token_index < len(token_list) and ("-" in get_value(token_list[self.token_index]) or "~" in get_value(token_list[self.token_index])):
                appnd_to_list(ident_space)
                compile_term(ident_space + 2)
            elif self.token_index < len(token_list) and "(" in get_value(token_list[self.token_index]):
                appnd_to_list(ident_space)
                compile_expression(ident_space + 2)
                appnd_to_list(ident_space)
            elif self.token_index + 1 < len(token_list) and ("(" in get_value(token_list[self.token_index + 1]) or 
                    "." in get_value(token_list[self.token_index + 1])):
                compile_subroutine_call(ident_space)
            else:
                appnd_to_list(ident_space)

            final_list.append(_add_identation(ident_space,"</term>"))

        def compile_expression_list(ident_space):
            """
            Function for compiling expression list token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """ 
            
            final_list.append(_add_identation(ident_space,"<expressionList>"))

            while self.token_index < len(token_list) and ")" not in get_value(token_list[self.token_index]):
                compile_expression(ident_space + 2)

                while self.token_index < len(token_list) and "," in get_value(token_list[self.token_index]):
                    appnd_to_list(ident_space)
                    compile_expression(ident_space + 2)

            final_list.append(_add_identation(ident_space,"</expressionList>"))

        final_list = []
        self.token_index = 0
        ident_space = 0 
        compile_class(ident_space)

        return final_list

    def parse_tokens(self):
        
        token_list = self._read_and_parse_t()
        final_list = self._parse_tokens(token_list)

        return final_list