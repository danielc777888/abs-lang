#A parser for the ABS language. By default it uses the SLR algorithm.
#Can be specified to use LALR(1). View ply1.5/doc/ply.html
import yacc
import abslexer
import absvisitors
import sys

#list of errors
errors =[]

#Generic node class for abstract parse tree
class Node:
    def __init__(self,type,lineNo,nonTerminals=None,terminals=None):
        self.type = type
        self.lineNo = lineNo
        if nonTerminals:
            self.nonTerminals = nonTerminals
        else:
            self.nonTerminals = []
        if terminals:
            self.terminals = terminals
        else:
            self.terminals = []
            
    
#Accepts visitor by reflectively calling appropriate method on visitor,
#visit_* method is determined by node type.eg.visit_identifier
    def accept(self,visitor):
        visitMethod = getattr(visitor,'visit_%s' % self.type)
        if visitMethod != None:
             visitMethod(self)
        return

#Get token map from lexer
tokens = abslexer.tokens

#Used to prevent shift-reduce conflicts.
#All are left associative. TIMES and DIVIDE have precedence over the rest
#since they are higher in the precedence spec.
precedence = (
    ('left','AND','OR'),
    ('left','EQUAL','NOT_EQ','GREATER','GREATER_EQ','LESS','LESS_EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
 )

def p_program(p):
    'program : start method_list'
    p[0] = Node('program',p.lineno(0),[p[1],p[2]],None)
    pass
    
def p_method_list_1(p):
    'method_list : method'
    p[0] = p[1]
    pass
    
def p_method_list_2(p):
    'method_list : method_list method'
    p[0] = Node('method_list',p.lineno(0),[p[1],p[2]],None)
    pass
    
def p_method_list_3(p):
    '''method_list : empty'''
    pass
    
def p_method_1(p):
    'method : CAN IDENTIFIER LPAREN parameter_list RPAREN GIVES type LANGLE statement_list RANGLE'
    p[0] = Node('method',p.lineno(0),[p[4],p[9]],[p[2],p[7]])
    pass
    
def p_method_2(p):
    'method : CAN IDENTIFIER LPAREN parameter_list RPAREN LANGLE statement_list RANGLE'
    p[0] = Node('method',p.lineno(0),[p[4],p[7]],[p[2],None])
    pass
    
def p_parameter_list_1(p):
    'parameter_list : parameter_list COMMA parameter'
    p[0] = Node('parameter_list',p.lineno(0),[p[1],p[3]],None)
    pass
    
def p_parameter_list_2(p):
    'parameter_list : parameter'
    p[0] = p[1]
    pass
    
def p_parameter_1(p):
    'parameter : type IDENTIFIER'
    p[0] = Node('parameter',p.lineno(0),None,[p[1],p[2]])
    pass
    
def p_parameter_2(p):
    '''parameter : empty'''
    pass
 
def p_start(p):
    'start : START LANGLE statement_list RANGLE'
    p[0] = Node('start',p.lineno(0),[p[3]],None)
    pass
    
def p_statement_list_1(p):
    'statement_list : statement'
    p[0] = p[1]
    pass

def p_statement_list_2(p):
    'statement_list : statement_list statement'
    p[0] = Node('statement_list',p.lineno(0),[p[1],p[2]],None)
    pass

def p_statement(p):
    '''statement : assignment_stmt
            |  array_stmt
            |  output_stmt
            |  input_stmt 
            |  if_stmt
            |  loop_stmt
            |  gives_stmt
            |  method_stmt'''
    p[0] =p[1]
    pass

def p_method_stmt(p):
    'method_stmt : method_call SEMI'
    p[0] =p[1]    

def p_gives_stmt(p):
    'gives_stmt : GIVES expression SEMI'
    p[0] =Node('gives_stmt',p.lineno(0),[p[2]],None)

def p_assignment_stmt_1(p):
    'assignment_stmt : type IDENTIFIER ASSIGN expression SEMI'
    p[0] = Node('assignment_stmt',p.lineno(0),[p[4]],[p[1],p[2]])
   
    
def p_assignment_stmt_2(p):
    'assignment_stmt : IDENTIFIER ASSIGN expression SEMI'
    p[0] = Node('assignment_stmt',p.lineno(0),[p[3]],[None,p[1]])
      
def p_array_stmt_1(p):
    'array_stmt : LISTOF IDENTIFIER ASSIGN LISTOF LPAREN expression COMMA type RPAREN SEMI'
    p[0] = Node('array_define',p.lineno(0),[p[6]],[p[2],p[8]])
   
    
def p_array_stmt_2(p):
    'array_stmt : IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression SEMI'
    p[0] = Node('array_assign',p.lineno(0),[p[3],p[6]],[p[1]])


def p_type(p):
    '''type : INT
        | TEXT
        '''
    p[0] = p[1]
    pass
    

def p_output_stmt(p):
    'output_stmt : OUTPUT LPAREN expression RPAREN SEMI'
    p[0] = Node('output_stmt',p.lineno(0),[p[3]],None)
    pass
    
def p_input_stmt_1(p):
    'input_stmt : IDENTIFIER ASSIGN INPUT LPAREN RPAREN SEMI'
    p[0] = Node('input_stmt',p.lineno(0),None,[p[1]])
    pass
    
def p_input_stmt_2(p):
    'input_stmt : type IDENTIFIER ASSIGN INPUT LPAREN RPAREN SEMI'
    p[0] = Node('input_stmt',p.lineno(0),None,[p[1],p[2]])
    pass
    
def p_if_stmt(p):
    'if_stmt : IF LPAREN expression RPAREN LANGLE statement_list RANGLE else_stmt'
    p[0] = Node('if_stmt',p.lineno(0),[p[3],p[6],p[8]],None)
    pass
    
def p_else_stmt_2(p):
    'else_stmt : ELSE LANGLE statement_list RANGLE'
    p[0] = Node('else_stmt',p.lineno(0),[p[3]],None)
    pass
    
def p_else_stmt_1(p):
    'else_stmt : empty'
    pass
    
def p_loop_stmt(p):
    'loop_stmt : WHILE LPAREN expression RPAREN LANGLE statement_list RANGLE'
    p[0] = Node('loop_stmt',p.lineno(0),[p[3],p[6]],None)
    pass

def p_expression_binop(p):
    '''expression : expression PLUS expression
                |   expression MINUS expression
                |   expression TIMES expression
                |   expression DIVIDE expression'''
                
    #if 2 integer literals than calculate
    if p[1].type == 'integer' and p[3].type == 'integer':
        num1 = p[1].terminals[0]
        num2 = p[3].terminals[0]
        operator = p[2]
        answer = 0;
        if operator == '+':
            answer = num1 + num2
        elif operator == '-':
            answer = num1 - num2
        elif operator == '*':
            answer = num1 * num2
        elif operator == '/':
            answer = num1 / num2
        p[0] = Node('integer',p.lineno(0),None,[answer])
    else:
        p[0] = Node('binop',p.lineno(0),[p[1],p[3]],[p[2]])
    pass
    
def p_expression_equality(p):
    '''expression : expression AND expression
                | expression OR expression
                | expression LESS expression
                | expression LESS_EQ expression
                | expression EQUAL expression
                | expression NOT_EQ expression
                | expression GREATER expression
                | expression GREATER_EQ expression'''
               
    p[0] = Node('equality',p.lineno(0),[p[1],p[3]],[p[2]])
    pass
    

    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]
    pass
    
def p_expression_integer(p):
    'expression : ILITERAL'
    p[0] = Node('integer',p.lineno(0),None,[p[1]])
    pass
    

def p_expression_text(p):
    'expression : TLITERAL'
    p[0] = Node('text',p.lineno(0),None,[p[1]])
    pass


def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = Node('identifier',p.lineno(0),None,[p[1]])
    pass
    
def p_expression_array(p):
    'expression : IDENTIFIER LBRACKET expression RBRACKET'
    p[0] = Node('array',p.lineno(0),[p[3]],[p[1]])
    
def p_expression_method_call(p):
    'expression : method_call'
    p[0] = p[1]
    
    
def p_method_call(p):
    'method_call : IDENTIFIER LPAREN expression_list RPAREN'
    p[0] = Node('method_call',p.lineno(0),[p[3]],[p[1]])
    
    
def p_expression_list_1(p):
    'expression_list : expression_list COMMA expression'
    p[0] = Node('expression_list',p.lineno(0),[p[1],p[3]],None)

def p_expression_list_2(p):
    'expression_list : expression'
    p[0] = p[1]
    
def p_expression_list_3(p):
    '''expression_list : empty'''
    pass

    
def p_empty(t):
    'empty : '
    pass
    

#Error rule for syntax errors
def p_error(p):
    errors.append("Syntax error in input : line %s" % (p.lineno))
    #read ahead while not reach closing '>'
    while 1:
        tok = yacc.token()
        if not tok or tok.type == 'RANGLE':break
    yacc.restart()
    #yacc.errok()
   

def parse(data):
    #build parser using SLR algorithm
    yacc.yacc()
    #parse data
    return yacc.parse(data) 
    
def has_errors():
    if len(errors) > 0:
        return True
    return False

#Entry point for testing
if __name__ == '__main__':
    
    if (len(sys.argv) < 2):
        print "Usage absparser.py <sourcefile>"
        sys.exit(1);
        
    #open test file
    f = open(sys.argv[1],'r')
    data = f.read()
    #build parser using SLR algorithm
    yacc.yacc()
    #parse data
    result = yacc.parse(data)
    if has_errors():
        for error in errors:
            print error
        sys.exit(1)
    visitor = absvisitors.PrintASTVisitor();
    if result is not None : visitor.visit(result)

