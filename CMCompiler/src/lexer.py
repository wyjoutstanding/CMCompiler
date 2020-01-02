#Tokens
tokens = (
    'IDENTIFIER', 'NUMBER', 'DIGIT_CONSTANT', 'STRING_CONSTANT',
    'ASSIGN', 'ADDRESS', 'LT', 'GT', 'SELF_PLUS', 'SELF_MINUS', 'PLUS', 'MINUS', 'MUL', 'DIV', 'GTE', 'LTE',
    'LL_BRACKET', 'RL_BRACKET', 'LB_BRACKET', 'RB_BRACKET', 'LM_BRACKET', 'RM_BRACKET', 'COMMA', 'DOUBLE_QUOTE', 'SEMICOLON', 'SHARP',
    'INCLUDE', 'INT', 'FLOAT', 'CHAR', 'DOUBLE', 'FOR', 'IF', 'ELSE', 'WHILE', 'DO', 'RETURN',
)

#Reserved words
reserved = {
    'include': 'INCLUDE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'return': 'RETURN'
}

#Operator
t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_ASSIGN = r'='
t_ADDRESS = r'&'
t_LT = r'<'
t_GT = r'>'
t_SELF_PLUS = r'\+\+'
t_SELF_MINUS = r'--'
t_LTE = r'<='
t_GTE = r'>='

#Separator
t_LL_BRACKET = r'\('
t_RL_BRACKET = r'\)'
t_LB_BRACKET = r'\{'
t_RB_BRACKET = r'}'
t_LM_BRACKET = r'\['
t_RM_BRACKET = r']'
t_COMMA = r','
t_DOUBLE_QUOTE = r'"'
t_SEMICOLON = r';'
t_SHARP = r'\#'

#Identifier
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')    # Check for reserved words
    return t

#Number
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

#Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex

lexer = lex.lex()
#str = '#include <cstdio>\nint a1a;\nint b1b;\na1a=1;\nb1b=2;\n'

str = open('../test/test1', 'r')
lexer.input(str.read())
while 1:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok.type, tok.value)