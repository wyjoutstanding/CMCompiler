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

noCollapse = 0

token_table = dict()

stack_offset = 0
lineno = 0

def addtwodimdict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
        return 1
    else:
        thedict.update({key_a:{key_b: val}})

class TokenType:
    pass

class Node:
    def __init__(self,type,val_type,children=None):
        self.type = type
        self.val_type = val_type
        self.val = ''
        if children:
            self.children = children
        else:
            self.children = [ ]

    def tra(self, num):
        ans =''
        if hasattr(self, 'type') == 0:
            ans += self
            print('\t'*num + '%s'%ans)
            return
        else:
            print('\t'*num + self.type)
            for i in self.children:
                if hasattr(i, 'type'):
                    i.tra(num+1)
                else:
                    ans = i
                    print('\t'*(num+1) + '%s'%ans)

    '''
    def __str__(self):
        ans = self.type+'\n'
        for i in self.children:
            if(hasattr(i, 'type')):
                ans+='\t'+i.__str__()
            else: ans+='\t'+i+'\n'
        return ans
    '''


def collapse(t):
    if((len(t) == 2) and (not noCollapse)):
        t[0]=t[1]
        return 1


def p_file(t):
    '''file : empty
            | file vardefine SEMICOLON'''

def p_vardefine(t):
    '''vardefine : type defineList'''


def p_defineList(t):
    '''defineList : defineElem'''


def p_defineElem(t):
    '''defineElem : IDENTIFIER'''
    if token_table.__contains__(t[1]):
        if token_table[t[1]]['is_define']==1:
            print("%d: Variable %s repetition definition\n"%(lineno, t[1]))
            return
    else:
        addtwodimdict(token_table, t[1], 'is_define', 1)
        addtwodimdict(token_table, t[1], 'var_type', 'int')
        addtwodimdict(token_table, t[1], 'name', t[1])
        print("push 0\n")
        #print(token_table[t[1]].address, "[ebp - %d]", ++stack_offset * 4)

def p_type(t):
    '''type : INT'''

def p_empty(t):
    '''empty : '''

def p_error(t):
    if t:
        print("Syntax error at '%s' (Line %d)" % (t.value, t.lineno))
    else:
        print("Syntax error at EOF")


import ply.yacc as yacc
parser = yacc.yacc(method='LALR')

f = open('../test/test2', 'r')
#parser.input(str.read())
while 1:
    line = f.readline()
    if line:
        parser.parse(line)
    else:
        break
print(token_table)
f.close()


#print(o.type)
#print(hasattr(o.children[1], 'type'))
#print(o.children[0].type)
#print(o.children[0].children)
#print('t:', o.type)
#print(o.val)
#print(o.val_type)



