from SymbolTable import SymbolTable
from VMWriter import VMWriter
from Lexicon import Lexicon

class CompilationEngine:
    """
    Class that reads the tokenized XML, and convertes it to
    the final XML.
    """

    token_index = 0
    symbol_table = None
    class_name = ''
    vm_writer = None
    while_num = 0

    def __init__(self, filename):
        self.filename = filename
        self.vm_writer = VMWriter(filename.replace('T.xml', '.vm'))
        self.symbol_table = SymbolTable()

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

    def advance(self):
        self.token_index += 1

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

        def get_type(value):

            return value[1:].split('>')[0]

        def parse_string_token(value):
            return value[17:].split('<')[0][0:-1]

        def compile_class(ident_space):
            """
            Function for compiling class token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            #final_list.append(_add_identation(ident_space,"<class>"))
            class_name = get_value(token_list[self.token_index + 1])
            self.class_name = class_name

            for i in range(0 , 3):
                self.advance()
                #appnd_to_list(ident_space)
            while self.token_index < len(token_list) and ("static" in get_value(token_list[self.token_index]) or "field" in get_value(token_list[self.token_index])):
                compile_class_var_dec(ident_space + 2, class_name)

            while self.token_index < len(token_list) and ("constructor" in get_value(token_list[self.token_index]) or 
                    "function" in get_value(token_list[self.token_index]) or "method" in get_value(token_list[self.token_index])):
                compile_subroutine(ident_space + 2, class_name)

            #appnd_to_list(ident_space)
            self.advance()

            #final_list.append(_add_identation(ident_space,"</class>"))


        def compile_class_var_dec(ident_space, class_name = ''):
            """
            Function for compiling class var dec token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
    
            #final_list.append(_add_identation(ident_space,"<classVarDec>"))
            #appnd_to_list(ident_space)
            token_kind = get_value(token_list[self.token_index])
            self.advance()
            token_type = get_value(token_list[self.token_index])
            self.advance()

            while self.token_index < len(token_list) and ";" not in get_value(token_list[self.token_index]):

                token_name = get_value(token_list[self.token_index])
                if token_name != ',':
                    self.symbol_table.define(token_name, token_type, token_kind)
                
                self.advance()
                #print(token_kind + " " + token_type)

            #print(self.symbol_table.class_table )
            #appnd_to_list(ident_space)
            self.advance()
            
            #final_list.append(_add_identation(ident_space,"</classVarDec>"))

        def compile_subroutine(ident_space, class_name=''):
            """
            Function for compiling subroutine token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            subroutine_type = get_value(token_list[self.token_index])
            #print(subroutine_type)
            self.symbol_table.startSubroutine()
            
            #final_list.append(_add_identation(ident_space,"<subroutineDec>"))
            self.advance()
            self.advance()
            if class_name:
                subroutine_name = '{}.{}'.format(class_name, get_value(token_list[self.token_index]))
            else:
                subroutine_name = get_value(token_list[self.token_index])

            self.advance()
            self.advance()
                #appnd_to_list(ident_space)

            compile_parameter_list(ident_space + 2)
            self.advance()


            #print(get_value(token_list[self.token_index]))

            #appnd_to_list(ident_space)

            compile_subroutine_body(ident_space + 2, subroutine_type, subroutine_name)
            compile_statements(ident_space, class_name)
            self.advance()


            #final_list.append(_add_identation(ident_space,"</subroutineDec>"))
        

        def compile_subroutine_body(ident_space, subroutine_type, subroutine_name):
            """
            Function for compiling subroutine body token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """            

            #final_list.append(_add_identation(ident_space,"<subroutineBody>"))

            #appnd_to_list(ident_space)
            self.advance() #{
            #print(get_value(token_list[self.token_index]))
            #print(get_value(token_list[self.token_index]))
            #print(get_value(token_list[self.token_index]))

            num_locals = compile_var_dec(ident_space)


            #print(num_locals)
            if subroutine_type == 'method':
                num_locals += 0
            
            self.vm_writer.write_function(subroutine_name, num_locals)
            
            if subroutine_type == 'constructor':
                self.vm_writer.write_push('constant', self.symbol_table.varCount('this'))
                self.vm_writer.write_call('Memory.alloc', 1)
                self.vm_writer.write_pop('pointer', 0)

            
            if subroutine_type == 'method':
                self.vm_writer.write_push('argument', 0)
                self.symbol_table.refactor()
                self.vm_writer.write_pop('pointer', 0)


        def compile_parameter_list(ident_space):
            """
            Function for compiling parameter list token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """     

            # final_list.append(_add_identation(ident_space,"<parameterList>"))
            #print(get_value(token_list[self.token_index]))

            while self.token_index < len(token_list) and ")" not in get_value(token_list[self.token_index]):
                
                token_type = get_value(token_list[self.token_index])
                self.advance()
                
                token_name = get_value(token_list[self.token_index])

                self.symbol_table.define(token_name, token_type, 'argument')
                self.advance()

                while self.token_index < len(token_list) and "," in get_value(token_list[self.token_index]):
                    #appnd_to_list(ident_space)
                    self.advance()
                    token_type = get_value(token_list[self.token_index])
                    self.advance()                    
                    token_name = get_value(token_list[self.token_index])
                    self.symbol_table.define(token_name, token_type, 'argument')
                    self.advance()

                    

            #final_list.append(_add_identation(ident_space,"</parameterList>"))

        def compile_var_dec(ident_space):
            """
            Function for compiling var dec token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """        
            
            if get_value(token_list[self.token_index]) != 'var':
                return 0

            #final_list.append(_add_identation(ident_space,"<varDec>"))

            self.advance()           
            token_type = get_value(token_list[self.token_index])
            self.advance()
            token_name = get_value(token_list[self.token_index])
            #print(token_name)
            self.advance()
            self.symbol_table.define(token_name, token_type, 'var')
            #print(self.symbol_table.subroutine_table)

            num_vars = 1
            #print(get_value(token_list[self.token_index]))

            while self.token_index < len(token_list) and ";" not in get_value(token_list[self.token_index]):

                self.advance()
                token_name = get_value(token_list[self.token_index])
                self.symbol_table.define(token_name, token_type, 'var')
                self.advance()
                num_vars += 1

            #appnd_to_list(ident_space)
            self.advance()
        
            num_vars += compile_var_dec(ident_space)
            #final_list.append(_add_identation(ident_space,"</varDec>"))
            return num_vars
        

        def compile_statements(ident_space, class_name = ''):
            """
            Function for compiling statements token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            #final_list.append(_add_identation(ident_space,"<statements>"))

            while self.token_index < len(token_list) and "}" not in get_value(token_list[self.token_index]):
                if self.token_index < len(token_list) and "let" in get_value(token_list[self.token_index]):
                    compile_let(ident_space + 2)
                elif self.token_index < len(token_list) and "if" in get_value(token_list[self.token_index]):
                    compile_if(ident_space + 2)
                elif self.token_index < len(token_list) and "while" in get_value(token_list[self.token_index]):
                    compile_while(ident_space + 2)
                elif self.token_index < len(token_list) and "do" in get_value(token_list[self.token_index]):
                    compile_do(ident_space + 2, class_name)
                elif self.token_index < len(token_list) and "return" in get_value(token_list[self.token_index]): 
                    compile_return(ident_space + 2)
            #final_list.append(_add_identation(ident_space,"</statements>"))

        def compile_do(ident_space, class_name = ''):
            """
            Function for compiling do token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            
            self.advance()
            #final_list.append(_add_identation(ident_space,"<doStatement>"))

            #appnd_to_list(ident_space)
  

            compile_subroutine_call(ident_space, class_name)          
            self.vm_writer.write_pop('temp', 0)
            

            self.advance()
            #and_to_list(ident_space)

            #final_list.append(_add_identation(ident_space,"</doStatement>"))

        def compile_subroutine_call(ident_space, class_name = ''):
            
            """
            Function for compiling subroutine call token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            subroutine_name = get_value(token_list[self.token_index])

            self.advance()
            if self.token_index + 1 < len(token_list) and "." in get_value(token_list[self.token_index]):
                subroutine_name += '.'
                self.advance()

                subroutine_name += get_value(token_list[self.token_index])
                self.advance()

                add_arg = False
            else:
                add_arg = True
            
            self.advance()
            #print(get_value(token_list[self.token_index]))

            num_args = compile_expression_list(ident_space)
            if add_arg:
                num_args += 1

            if '.' not in subroutine_name:
                subroutine_name = self.class_name + '.' + subroutine_name    


            if self.class_name in subroutine_name and 'new' not in subroutine_name and self.class_name != 'Main':
                #print(subroutine_name)
                self.vm_writer.write_push('pointer', 0)

            if self.symbol_table.indexOf(subroutine_name.split('.')[0]) != None:

                self.vm_writer.write_push('this', self.symbol_table.indexOf(subroutine_name.split('.')[0]))
                subroutine_name = subroutine_name[0].upper() + subroutine_name[1:]
                num_args += 1
                self.vm_writer.write_call(subroutine_name, num_args)
            else:
                subroutine_name = subroutine_name[0].upper() + subroutine_name[1:]    
                self.vm_writer.write_call(subroutine_name, num_args)
            
            #print(get_value(token_list[self.token_index]))        
            self.advance()


        def compile_let(ident_space):
            """
            Function for compiling let token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            
            #final_list.append(_add_identation(ident_space,"<letStatement>"))

            self.advance()
            symbol = get_value(token_list[self.token_index])
            kind = self.symbol_table.kindOf(symbol)
            index = self.symbol_table.indexOf(symbol)
            self.advance()

            if self.token_index < len(token_list) and "[" in get_value(token_list[self.token_index]):
                
                #appnd_to_list(ident_space)
                self.advance()
                compile_expression(ident_space + 2)
                self.vm_writer.write_push(kind, index)

                self.advance()
                self.vm_writer.write_arithmetic('add')
                self.advance()
                compile_expression(ident_space)
                self.vm_writer.write_pop('temp', 0)  # store expression in temp 0
                self.vm_writer.write_pop('pointer', 1)  # NOQA store the register location of the array in 'that'
                self.vm_writer.write_push('temp', 0)
                self.vm_writer.write_pop('that', 0)
            else:
                self.advance()
                compile_expression(ident_space)
                self.vm_writer.write_pop(kind, index)


                #appnd_to_list(ident_space)
            self.advance()


        def compile_while(ident_space):
            """
            Function for compiling while token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """

            #final_list.append(_add_identation(ident_space,"<whileStatement>"))

            self.advance()
            while_expression_label = 'WHILE_{}'.format(self.while_num)
            while_continuation_label = 'WHILE_END_{}'.format(self.while_num)
            self.while_num += 1
            self.vm_writer.write_label(while_expression_label)

            self.advance()

            compile_expression(ident_space + 2)

            self.advance()

            self.vm_writer.write_arithmetic('not')
            self.vm_writer.write_if(while_continuation_label)
            

            self.advance()
            compile_statements(ident_space + 2)
            self.vm_writer.write_goto(while_expression_label)
            self.vm_writer.write_label(while_continuation_label)
            self.advance()
           # appnd_to_list(ident_space)

            #final_list.append(_add_identation(ident_space,"</whileStatement>"))

        def compile_return(ident_space):
            
            """
            Function for compiling return token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            #final_list.append(_add_identation(ident_space,"<returnStatement>"))

            #appnd_to_list(ident_space)
            self.advance()

            if self.token_index < len(token_list) and ";" not in get_value(token_list[self.token_index]):
                compile_expression(ident_space + 2)
            else:
                self.vm_writer.write_push('constant', 0)

            #appnd_to_list(ident_space)
            self.advance()

            #final_list.append(_add_identation(ident_space,"</returnStatement>"))
            self.vm_writer.write_return()

        def compile_if(ident_space):
            """
            Function for compiling if token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """    
            
            label_if_true = 'IF_TRUE_{}'.format(self.while_num)
            label_if_false = 'IF_FALSE_{}'.format(self.while_num)
            label_if_contiuation = 'IF_CONTINUATION_{}'.format(self.while_num)
            
            self.while_num += 1

            self.advance()

            self.advance()             

            compile_expression(ident_space + 2)

            self.vm_writer.write_if(label_if_true)
            self.vm_writer.write_goto(label_if_false)
            self.vm_writer.write_label(label_if_true)
            self.advance()
            self.advance()

            compile_statements(ident_space)
            self.vm_writer.write_goto(label_if_contiuation)

            self.advance()
            
            else_flag = False

            if self.token_index < len(token_list) and "else" in get_value(token_list[self.token_index]):

                else_flag = True

                self.vm_writer.write_label(label_if_false)

                self.advance()

                self.advance()

                compile_statements(ident_space + 2)

                self.advance()

                #appnd_to_list(ident_space)

           #final_list.append(_add_identation(ident_space,"</ifStatement>"))

            if not else_flag:
                self.vm_writer.write_label(label_if_false)

            self.vm_writer.write_label(label_if_contiuation)

        def compile_expression(ident_space):
            
            """
            Function for compiling expressiong token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            #final_list.append(_add_identation(ident_space,"<expression>"))

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
                #appnd_to_list(ident_space)
                #print(get_value(token_list[self.token_index]))
                token_val = get_value(token_list[self.token_index])
                self.advance()
                compile_term(ident_space + 2)
                if token_val == '*':
                    self.vm_writer.write_call('Math.multiply', 2)
                elif token_val == '/':
                    self.vm_writer.write_call('Math.divide', 2)
                else:
                    command = {
                    '+': 'add',
                    '-': 'sub',
                    '&amp;': 'and',
                    '|': 'or',
                    '&lt;': 'lt',
                    '&gt;': 'gt',
                    '=': 'eq'
                    }[token_val]
                    self.vm_writer.write_arithmetic(command)

            #final_list.append(_add_identation(ident_space,"</expression>"))


        def compile_term(ident_space):
            """
            Function for compiling term token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """
            term_keywords = ['true', 'false', 'null', 'this']


            #final_list.append(_add_identation(ident_space,"<term>"))
            if self.token_index + 1 < len(token_list) and "[" in get_value(token_list[self.token_index + 1]):
                token_val = get_value(token_list[self.token_index])
                kind = self.symbol_table.kindOf(token_val)
                index = self.symbol_table.indexOf(token_val)
                self.advance()
                self.advance()
                compile_expression(ident_space)
                self.vm_writer.write_push(kind, index)

                self.vm_writer.write_arithmetic('add')
                self.vm_writer.write_pop('pointer', 1)
                self.vm_writer.write_push('that', 0)
                self.advance()
                
            elif get_value(token_list[self.token_index]).isdigit():
                token_val = get_value(token_list[self.token_index])

                self.advance()
                self.vm_writer.write_push('constant', token_val)


            elif get_value(token_list[self.token_index]) in term_keywords:
                if get_value(token_list[self.token_index]) in ['false', 'null']:
                    self.vm_writer.write_push('constant', 0)
                elif get_value(token_list[self.token_index]) == 'true':
                    self.vm_writer.write_push('constant', 0)
                    self.vm_writer.write_arithmetic('not')
                else:  # this command
                    self.vm_writer.write_push('pointer', 0)
                self.advance()  # _self.vm_writer.write_token(file, _pop(token_stack))
                
      

            elif self.token_index < len(token_list) and ("-" in get_value(token_list[self.token_index]) or "~" in get_value(token_list[self.token_index])):
                token_val = get_value(token_list[self.token_index])
                self.advance()
                #appnd_to_list(ident_space) 
                compile_term(ident_space + 2)
                command = {'-': 'neg', '~': 'not'}[token_val]
                self.vm_writer.write_arithmetic(command)

            elif self.token_index < len(token_list) and "(" in get_value(token_list[self.token_index]):
                    self.advance()
                    compile_expression(ident_space)
                    self.advance()  # _self.vm_writer.write_token(file, _pop(token_stack))

            elif self.token_index + 1 < len(token_list) and ("(" in get_value(token_list[self.token_index + 1]) or 
                    "." in get_value(token_list[self.token_index + 1])):
                compile_subroutine_call(ident_space)

            elif get_type(token_list[self.token_index]) == 'stringConstant':
                token_val = parse_string_token(token_list[self.token_index])
                self.advance()                

                # _self.vm_writer.write_token(file, _pop(token_stack))
                
                self.vm_writer.write_push('constant', len(token_val))
                self.vm_writer.write_call('String.new', 1)
                for letter in token_val:
                    self.vm_writer.write_push('constant', ord(letter))
                    self.vm_writer.write_call('String.appendChar', 2)

            else:
                token_val = get_value(token_list[self.token_index])
                kind = self.symbol_table.kindOf(token_val)
                index = self.symbol_table.indexOf(token_val)
                self.vm_writer.write_push(kind, index)
                self.advance()

            #final_list.append(_add_identation(ident_space,"</term>"))

        def compile_expression_list(ident_space):
            """
            Function for compiling expression list token.

            @type ident_space: int
            @param ident_space: space units to be added

            @returns: None
            """ 
            num_args = 0

            if self.token_index < len(token_list) and ")" not in get_value(token_list[self.token_index]):
                compile_expression(ident_space + 2)
                num_args += 1

                while self.token_index < len(token_list) and "," in get_value(token_list[self.token_index]):
                    #appnd_to_list(ident_space)
                    self.advance()
                    compile_expression(ident_space + 2)
                    num_args += 1

            return num_args

        final_list = []
        self.token_index = 0
        ident_space = 0 
        compile_class(ident_space)

        return final_list

    def parse_tokens(self):
        
        token_list = self._read_and_parse_t()
        final_list = self._parse_tokens(token_list)
        self.vm_writer.close()
        return final_list