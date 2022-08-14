#A lexer for ABS language
import lex
import sys

#list for errors
errors = []

#Reserved words
reserved = ( 'START','INT','OUTPUT','INPUT','TEXT','IF','ELSE','AND','OR',
'WHILE','LISTOF','CAN','GIVES')

#Tokens
tokens = reserved + (
#Literals
    'IDENTIFIER','ILITERAL','TLITERAL',
#Operators
    'PLUS','MINUS','TIMES','DIVIDE','LESS','GREATER','EQUAL','GREATER_EQ',
    'LESS_EQ','NOT_EQ',
    
#Assignment
    'ASSIGN',
#Delimiters
    'LPAREN','RPAREN','SEMI','LANGLE','RANGLE','LBRACKET','RBRACKET','COMMA'
    )

#Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'

#Assignment Operators
t_ASSIGN = r'='

#Delimiters
t_LPAREN = '\('
t_RPAREN = '\)'
t_SEMI = ';'
t_LANGLE = '<'
t_RANGLE = '>'
t_LBRACKET = '\['
t_RBRACKET = '\]'
t_COMMA = ','


#Completely ignored characters
t_ignore = ' \t'

#New lines
def t_newline(t):
    r'\n+'
    t.lineno += t.value.count('\n')

#Handle comments
def t_comment(t):
    #Support single and multi-line comments
    r'(\#[^#](.)*\n) | (\#\#(.|\n)*?\#\#)'
    t.lineno += 1
    

#Handle all unrecognized tokens
def t_error(t):
    errors.append('Illegal character %s : line %s' %  (repr(t.value[0]),t.lineno))
    t.skip(1)
        
#Convert reserved tokens to lower case to match with keywords
reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

#Handle equality tokens before IDENTIFIER token
def t_EQUAL(t):
    r'is='
    return t;

def t_NOT_EQ(t):
    r'isnot='
    return t;
    
def t_LESS_EQ(t):
    r'is<='
    return t;
    
def t_LESS(t):
    r'is<'
    return t;
    
def t_GREATER_EQ(t):
    r'is>='
    return t;
    
def t_GREATER(t):
    r'is>'
    return t;
    


#Identifier tokens
def t_IDENTIFIER(t):
    r'[a-zA-Z_][\w_]*'
    #if not a reserved keyword then token is an IDENTIFIER
    t.type = reserved_map.get(t.value,'IDENTIFIER')
    return t
 
#Integer literal   
def t_ILITERAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer literal %s is not valid!" % t.value
        t.value = 0
    return t
    
#text literal
def t_TLITERAL(t):
    r'\'(.|\n)*?[^\\]\''
    t.value = str(t.value.strip('\''))
    return t

#build lexer
lex.lex()

#Entry point for testing
if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print "Usage : abslexer.py <sourcefile>"
        sys.exit(1)
    #open test file
    f = open(sys.argv[1],'r')
    data = f.read()
    #give input
    lex.input(data)
    #tokenize
    while 1:
        tok = lex.token()
        if not tok:break
        print tok



