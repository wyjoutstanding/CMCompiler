import ply.yacc as yacc
from lexer import tokens


start = 'start_state'
token_table = dict()
reg = {'eax':0, 'edx':0}
n = 0                 # IR式标号
label = 0             # LABEL 标号
tad = []
while_list = []
ass =[]
flag = 0
temp = 1              # 临时变量标号
flag1 =0

def addtwodimdict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
        return 1
    else:
        thedict.update({key_a:{key_b: val}})

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


s = Stack()  #存放临时变量的栈


def p_start_state(p):
    'start_state : INT ID OPBRAC  CLOSEBRAC stmts'
    global result
    result = 'Valid'

def p_iter_stmt(p):
    '''iter_stmt : X Y Z '''
    global n

def p_X(p):
    '''X : IF  OPBRAC cond_stmt  CLOSEBRAC '''
    global n
    global s
    global label
    z = "L" + str(label)
    k = str(s.pop())
    s.push(z)

    if (p[1] == "if"):
        tad.append('('+"JNT,"+ k +",_,"+ z+')')
        n += 1

def p_Y(p):
    '''Y : stmts '''
    global n
    global label
    label += 1
    k = "L" + str(label)
    tad.append('('+'JMP,_,_,'+k+')')
    n += 1
    m = str(s.pop())
    tad.append('('+'LABEL,'+m+',_,_'+')')
    n += 1
    s.push(k)
    label += 1

def p_Z(p):
    '''Z : ELSE stmts'''
    global n
    global label
    k = str(s.pop())
    tad.append('('+'LABEL,' + k + ',_,_'+')')
    n += 1

def p_while_stmt(p):
    '''while_stmt : XX YY'''
    global n

def p_XX(p):
    '''XX : WHILE  OPBRAC whilecond_stmt  CLOSEBRAC '''
    global n
    global s
    global label
    z = "L" + str(label+1)
    k = str(s.pop())
    s.push(z)

    if (p[1] == "while"):
        tad.append('('+"JNT,"+ k +",_,"+ z+')')
        n+=1

def p_YY(p):
    '''YY : DO whilestmts '''
    global n
    global label
    k = "L" + str(label)
    tad.append('('+'JMP,_,_,'+k+')')
    m = str(s.pop())
    tad.append('('+'LABEL,'+m+',_,_'+')')
    n+=2

def p_whilecond_stmt(p):
    '''whilecond_stmt : ID RELOP ID
            | ID RELOP NUMBER
            | NUMBER RELOP ID
            | NUMBER RELOP NUMBER
            | whilecond_stmt LOGOP whilecond_stmt
            |'''
    global temp
    global n
    global label
    global flag1
    if flag1==0:
        z = 'L' + str(label)
        tad.append('(' + 'LABEL,' + z + ',_,_' + ')')
        flag1=1
    m = "t" + str(temp)
    if (p[2] == "&&"):
        z = s.pop()
        k = s.pop()
        tad.append('('+'AND'+','+k+','+z+','+m+')')
        s.push(m)
    elif (p[2] == "||"):
        z = s.pop()
        k = s.pop()
        tad.append('(' + 'OR' + ',' + k + ',' + z +','+ m + ')')
        s.push(m)
    else:
        tad.append('(' +p[2]+','+p[1]+','+p[3]+','+m+')')
        s.push(m)

    temp += 1
    n += 2

def p_stmts(p):
    '''stmts : OPENFLR stmts CLOSEFLR
            | iter_stmt stmts
            | while_stmt stmts
            | expr_stmt STATETER stmts
            | declareint STATETER stmts
            | math stmts
            | newone stmts
            | '''

def p_whilestmts(p):
    '''whilestmts : OPENFLR whilestmts CLOSEFLR
                | iter_stmt
                | while_stmt
                | expr_stmt STATETER whilestmts
                | declareint STATETER whilestmts
                | math whilestmts
                | newone whilestmts
                | '''

def p_newone(p):
    '''newone : ID ASSIGN ID PLUS NUMBER STATETER stmts
                   | ID ASSIGN ID PLUS ID STATETER stmts
                   |  ID ASSIGN ID MINUS NUMBER STATETER stmts
                   |  ID ASSIGN ID MINUS ID STATETER stmts'''
    global temp
    global n
    m = "t" + str(temp)
    if (p[4] == "+" and p[2] == "="):
        tad.append('('+'+,'+p[3]+','+p[5]+','+m+')')
        tad.append('('+'=,' + m + ',_,' + p[1]+')')
        temp += 1
        n += 2
    elif (p[4] == "-" and p[2] == "="):
        tad.append('('+'-,' + p[3] + ',' + p[5] + ',' + m+')')
        tad.append('('+'=,' + m + ',_,' + p[1]+')')
        temp += 1
        n += 2


def p_expr_stmt(p):
    '''expr_stmt : assignment_int
            | declare'''


def p_assignment_int(p):
    '''assignment_int : INT ID ASSIGN NUMBER followint'''
    tad.append('('+'=,' + p[4] + ',_,' + p[2]+')')
    global n
    n = n + 1


def p_assignment_int1(p):
    '''assignment_int : INT ID  followint'''


def p_follow_int(p):
    '''followint : COMMA ID ASSIGN NUMBER followint'''
    tad.append('('+'=,' + p[4] + ',_,' + p[2]+')')
    global n
    n = n + 1


def p_follow_int1(p):
    '''followint : COMMA ID  followint'''


def p_follow_int2(p):
    '''followint : '''

def p_declare(p):
    '''declare : ID ASSIGN NUMBER followint'''
    tad.append('('+'=,' + p[3] + ',_,' + p[1]+')')
    global n
    n = n + 1


def p_declareint(p):
    '''declareint : ID ASSIGN NUMBER '''
    print("-------------", p[1])
    tad.append('('+'=,' + p[3] + ',_,' + p[1]+')')
    global n
    n = n + 1

def p_cond_stmt(p):
    '''cond_stmt : ID RELOP ID
            | ID RELOP NUMBER
            | NUMBER RELOP ID
            | NUMBER RELOP NUMBER
            | cond_stmt LOGOP cond_stmt
            |'''
    global temp
    global n
    m = "t" + str(temp)
    if (p[2] == "&&"):
        z = s.pop()
        k = s.pop()
        tad.append('('+'AND'+','+k+','+z+','+m+')')
        s.push(m)
    elif (p[2] == "||"):
        z = s.pop()
        k = s.pop()
        tad.append('(' + 'OR' + ',' + k + ',' + z +','+ m + ')')
        s.push(m)
    else:
        tad.append('(' +p[2]+','+p[1]+','+p[3]+','+m+')')
        s.push(m)

    n = n + 1
    temp += 1


def p_math(p):
    '''math : ID PLUS ASSIGN NUMBER STATETER
            | ID PLUS ASSIGN ID STATETER
            | ID MINUS ASSIGN NUMBER STATETER
            | ID MINUS ASSIGN ID STATETER
            | ID AOP ASSIGN NUMBER STATETER
            | ID AOP ASSIGN ID STATETER
            | PLUS PLUS ID STATETER
            | ID PLUS PLUS STATETER
            | MINUS MINUS ID STATETER
            | ID MINUS MINUS STATETER
            '''
    global temp
    global n
    m = "t" + str(temp)
    if (p[2] == "+" and p[3] == "="):
        tad.append('('+'+,' + p[1] + ',' + p[4] + ',' + m+')')
        tad.append('('+'=,' + m + ',_,' + p[1]+')')
        temp += 1
        n += 2
    elif (p[2] == "-" and p[3] == "="):
        tad.append('('+'-,' + p[1] + ',' + p[4] + ',' + m+')')
        tad.append('('+'=,' + m + ',_,' + p[1]+')')
        temp += 1
        n += 2
    elif (p[2] == "/" and p[3] == "="):
        tad.append('('+'/,' + p[1] + ',' + p[4] + ',' + m+')')
        tad.append('('+'=,' + m + ',_,' + p[1]+')')
        temp += 1
        n += 2
    elif (p[2] == "*" and p[3] == "="):
        tad.append('('+'*,' + p[1] + ',' + p[4] + ',' + m+')')
        tad.append('('+'=,' + m + ',_,' + p[1]+')')
        temp += 1
        n += 2
    elif (p[2] == "%" and p[3] == "="):
        tad.append('('+'%,' + p[1] + ',' + p[4] + ',' + m+')')
        tad.append('('+'=,' + m + ',_,' + p[1]+')')
        temp += 1
        n += 2
    elif ((p[1] == "+" and p[2] == "+") or (p[2] == "+" and p[3] == "+")):
        tad.append('+,' + p[1] + ',' + '1' + ',' + m)
        tad.append(('=,' + m + ',_,' + p[1]))
        temp += 1
        n += 2
    elif ((p[1] == "-" and p[2] == "-") or (p[2] == "-" and p[3] == "-")):
        tad.append('('+'-,' + p[1] + ',' + '1' + ',' + m+')')
        tad.append('('+'=,' +m + ',_,' + p[1]+')')
        temp += 1
        n += 2


def p_follow(p):
    ''' follow : COMMA ID follow
            |'''


def p_error(p):
    print("\n")
    print("Syntax error in input: %s line number:%s" % (p, str(p.lineno)))
    print("\n")

    # pass




result = 'Invalid'
parser = yacc.yacc()
program = open("../test/test2", 'r').read()


def parse(program):
    global parser
    global result
    res = parser.parse(program, tracking=True)
    return result


parse(program)

if flag == 1:
    print("Invalid")
else:
    print(result)
print("\n")
for i in range(n):
    print(tad[i])
