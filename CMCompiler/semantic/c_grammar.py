# =============================================================================
# 文件名：c_grammar.py
# 功能：基于python-lex和python-yacc的C-语法分析器
# 作者： 武起龙，张峥
# 时间：2019/12/29
#==============================================================================
# *接口说明*
#   - getGrammar() : 生成parsetab.py和parse.out文件
#
#
# *如何使用*
#   - 作为模块使用时注释/关闭末尾的测试代码，调用getGrammar即可
#
# *有用参考*
#   - 英文文档：http://www.dabeaz.com/ply/ply.html （强烈推荐）
#   - 中文文档：https://www.cnblogs.com/P_Chou/p/python-lex-yacc.html
# =============================================================================
# *实现思路*
#   1.输入标识符和界符等符号
#   2.定义注释和回车的忽略规则
#   3.设置递进规约规则
#   4.输入产生式列表
# =============================================================================

error_num = 0 #用于记录错误次数

# =============================================================================
# 1. tokens 列表定义
#   tokens必须要有，多于一个字符的终结符的命名写在这
#   里面的每个符号都要有对应正则定义,且以 t_ 开头，详细见后文 
# =============================================================================

tokens = (
    'INT','VOID','IF','ELSE','WHILE','RETURN','NUM','ID','GE','LE','EE','NE','ANNOTATION'
    )

# =============================================================================
# 1. literals 列表定义
#   一个字符的终结符的命名写在这
#   字符对应终结符，不需要正则定义 
# =============================================================================
literals = ['=','+','-','*','/', '(',')',';','<','>','{','}',',','[',']']
 
# =============================================================================
# 2.以下为各个token的正则表达式定义，采用 t_tokenName 的命名方式
# 若要对其进行运算，可通过定义函数的方式
# =============================================================================

t_INT = r'int'
t_VOID = r'void'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_RETURN = r'return'
t_ID    = r'(?!int|void|if|else|while|return)[a-zA-Z_][a-zA-Z0-9_]*'
t_NUM = r'[0-9]+'
t_GE = r'>='
t_LE = r'<='
t_EE = r'=='
t_NE = r'!='

#定义忽略注释的正则表达式
def t_ANNOTATION(t):
#    r'/\*([a-zA-Z0-9 _]|\r|\n|\t)*\*/' # 第一行写正则表达式
    r'(/\*(.|\n)*?\*/)|(\/\/.*)'
    t.lexer.lineno += t.value.count('\n') # 累计行数
    pass # 表示忽略该token

# 定义忽略字符的正则表达式，忽略空格回车换行

t_ignore = " \t\r"


#==============================================================================
# 通过函数定义正则表达式，可以增加额外动作，比如给value重新赋值，或增加其余字段信息
#==============================================================================

# 增加行数
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    pass

# 错误处理：输出错误符号，行数，列数后跳过当前错误继续扫描
def t_error(t):
    global error_num
    error_num += 1
    #print("Illegal character '%s'" % t.value[0])
    tmp = t.lexpos - data.rfind('\n',0,t.lexpos)
    print(f"========Illegal character: {t.value[0]}   line: {str(t.lineno)}   col: {str(tmp)}")
    #print("(%d," % t.lexer.lineno, "%d)" % t.lexer.lexpos)
    t.lexer.skip(1)

import ply.lex as lex # 导入python lex模块

lex.lex()# 调用Lex模块，构建词法分析器

# =============================================================================
# 符号表
# =============================================================================
class SymTabItem:
    def __init__(self, type=None, name=None, value=None):
        self.type = type
        self.name = name
        self.value = value
#a = SymTabItem(1,2,3)
symTab = dict()
#==============================================================================
#产生式列表
#==============================================================================
# 开始符号：program
def p_program_1(p):
    '''program : declaration_list'''
    
# 声明列表
def p_declaration_list_1(p):
    '''declaration_list : declaration_list declaration'''
def p_declaration_list_2(p):
    '''declaration_list : declaration'''
    
# 变量和函数声明
def p_declaration_1(p):
    '''declaration : var_declaration'''
def p_declaration_2(p):
    '''declaration : fun_declaration'''

# 变量声明具体定义：普通变量；一维数组
def p_var_declaration_1(p):
    '''var_declaration : type_specifier ID ';' '''
#    print(p[1]+" " +p[2])
    symTab[p[2]] = SymTabItem(p[1], p[2])
def p_var_declaration_2(p):
    '''var_declaration : type_specifier ID '[' NUM ']' ';' '''

# 变量/函数声明类型：INT;VOID
def p_type_specifier_1(p):
    '''type_specifier : INT'''
    p[0] = 'INT'
def p_type_specifier_2(p):
    '''type_specifier : VOID'''
    p[0] = 'VOID'

# 函数声明：头部；过程体
def p_fun_declaration_1(p):
    '''fun_declaration : type_specifier ID '(' params ')' compound_stmt'''
#def p_fun_declaration_2(p):
#    '''fun_declaration : compound_stmt'''

# 参数定义
def p_params_1(p):
    '''params : param_list'''
    p[0] = p[1]
def p_params_2(p):
    '''params : VOID'''
    p[0] = 'VOID'
def p_params_empty(p):
    '''params : '''

def p_param_list_1(p):
    '''param_list : param_list ',' param'''
def p_param_list_2(p):
    '''param_list : param'''
    p[0] = p[1]

def p_param_1(p):
    '''param : type_specifier ID'''
    p[0] = p[2]
def p_param_2(p):
    '''param : type_specifier ID '[' ']' '''
    p[0] = p[2]

# 函数体
def p_compound_stmt_1(p):
    '''compound_stmt : '{' local_declarations statement_list '}' '''

def p_local_declarations_1(p):
    '''local_declarations : local_declarations var_declaration'''
def p_local_declarations_empty(p):
    '''local_declarations : '''
# 语句列表
def p_statement_list_1(p):
    '''statement_list : statement_list statement'''
def p_statement_list_empty(p):
    '''statement_list : '''

# 表达式；符合语句；选择；循环；返回
def p_statement_1(p):
    '''statement : expression_stmt'''
def p_statement_2(p):
    '''statement : compound_stmt'''
def p_statement_3(p):
    '''statement : selection_stmt'''
def p_statement_4(p):
    '''statement : iteration_stmt'''
def p_statement_5(p):
    '''statement : return_stmt'''
    p[0] = p[1]
    if p[1] == 'VOID':
        printQtua(newLabel(), 'Return', '_', '_', '_')
    else:
        printQtua(newLabel(), 'Return', p[1], '_', '_')
        

# 表达式语句
def p_expression_stmt_1(p):
    '''expression_stmt : expression ';' '''
def p_expression_stmt_2(p):
    '''expression_stmt : ';' '''
# IF语句
def p_selection_stmt_1(p):
    '''selection_stmt : IF '(' expression ')' statement'''
def p_selection_stmt_2(p):
    '''selection_stmt : IF '(' expression ')' statement ELSE statement'''

# WHILE语句
def p_iteration_stmt_1(p):
    '''iteration_stmt : WHILE '(' expression ')' statement'''

# RETURN语句
def p_return_stmt_1(p):
    '''return_stmt : RETURN ';' '''
    p[0] = 'VOID'
def p_return_stmt_2(p):
    '''return_stmt : RETURN expression ';' '''
    p[0] = p[2]
# 表达式具体分解
def p_expression_1(p):
    '''expression : var '=' expression'''
    printQtua(newLabel(), p[2], p[3], '_', p[1]) # 先产生代码
    p[1] = p[3] # 直接赋值
def p_expression_2(p):
    '''expression : simple_expression'''
    p[0] = p[1]

# 变量：普通变量或数组
def p_var_1(p):
    ''' var : ID'''
    p[0] = p[1]
# 一维数组引用：a[m] => T = a[m*dataType.width]，[]中填偏移量
def p_var_2(p):
    ''' var : ID '[' expression ']' '''
    tmp1 = newTmp()
    printQtua(newLabel(), '*', p[3], '4', tmp1) # 偏移：T1 = expression.val * 4
    tmp2 = newTmp()
    p[0] = tmp2 # 其实并不需要记录tmp2的标号内有什么，只要记住他的索引即可
    printQtua(newLabel(), '[]', p[1], tmp1, tmp2) # 引用：T2 = ID[T1] 
#=====================================
# 以下为表达式定义：优先级：关系符 < 加减 < 乘除
# 简单表达式：关系表达式
def p_simple_expression_1(p):
    '''simple_expression : additive_expression relop additive_expression'''
def p_simple_expression_2(p):
    '''simple_expression : additive_expression'''
    p[0] = p[1]

def p_relop_1(p):
    '''relop : LE'''
def p_relop_2(p):
    '''relop : '<' '''
def p_relop_3(p):
    '''relop : '>' '''
def p_relop_4(p):
    '''relop : GE'''
def p_relop_5(p):
    '''relop : EE'''
def p_relop_6(p):
    '''relop : NE'''

# 四则运算：已考虑四则运算优先级
def p_additive_expression_1(p):
    '''additive_expression : additive_expression addop term'''
    p[0] = newTmp()
    printQtua(newLabel(), p[2], p[1], p[3], p[0])
def p_additive_expression_2(p):
    '''additive_expression : term'''
    p[0] = p[1]

# 关系符直接传递
def p_addop_1(p):
    '''addop : '+' '''
    p[0] = p[1]
def p_addop_2(p):
    '''addop : '-' '''
    p[0] = p[1]

# 生成代码
def p_term_1(p):
    '''term : term mulop factor'''
    p[0] = newTmp() # 新建标号
#    print(newLabel(),': ',(p[2], p[1], p[3], p[0]))
    printQtua(newLabel(), p[2], p[1], p[3], p[0])
    
def p_term_2(p):
    '''term : factor'''
    p[0] = p[1]
    
# 关系符直接传递
def p_mulop_1(p): 
    ''' mulop : '*' '''
    p[0] = p[1]
    
def p_mulop_2(p):
    ''' mulop : '/' '''
    p[0] = p[1]
    
# factor可以是表达式、简单变量，函数调用，常数
# 不产生代码
def p_factor_1(p):
    '''factor : '(' expression ')' '''
    p[0] = p[2]
    
def p_factor_2(p):
    '''factor : var'''
    p[0] = p[1]
    
def p_factor_3(p):
    '''factor : call'''
    
def p_factor_4(p):
    '''factor : NUM'''
    p[0] = p[1]
#    print('factor : NUM', p[1])

# 调用函数
def p_call_1(p):
    ''' call : ID '(' args ')' '''
    if p[3]: # 存在实参    
        for arg in p[3]: # 遍历实参，生成param代码
            printQtua(newLabel(), 'Param', arg, '_', '_')
    printQtua(newLabel(), 'Call', p[1], str(len(p[3])), '_') # 需输出函数名和参数个数
        
def p_args_1(p):
    '''args : arg_list'''
    p[0] = p[1]
def p_args_empty(p):
    '''args : '''
# 实参拼接
def p_arg_list_1(p):
    ''' arg_list : arg_list ',' expression'''
    p[0] = p[1] + p[3] # 拼接参数
#    print("arglist "+p[1],  "expression "+p[2], "p[0] " + p[0])
def p_arg_list_2(p):
    ''' arg_list : expression'''
    p[0] = p[1]
#    print("expression"+p[1])

#错误处理，输出错误所在单词
def p_error(p):
    global error_num
    error_num+=1
    if p:
        print("Syntax error at '%s'" %p.value," line:%d"%p.lexer.lineno)

    else:
        print("Syntax error at EOF")


# =============================================================================
# 产生标号，中间变量
# =============================================================================
labelNum = 0
tmpNum = 0
# 新建标号
def newLabel():
    global labelNum
    labelNum += 1
    return labelNum

# 新建中间变量
def newTmp():
    global tmpNum
    tmpNum += 1
    return 'T'+str(tmpNum)
code = [0] # 存放代码
# 打印四元式:标号，操作符，参数1，参数2，结果
def printQtua(labelNum=None, op='_', arg1='_', arg2='_', result='_'):
    code.append((op, arg1, arg2, result))
    print(str(labelNum)+') : ', (op, arg1, arg2, result))
# =============================================================================
# 接口：运行时生成相应的parse.out和parsetab.py文件供之后使用
# =============================================================================
import ply.yacc as yacc
def get_Grammar():
    yacc.yacc()

# =============================================================================
# 测试部分：真正运行时将其注释掉 / 将ISTEST设为False
# =============================================================================
ISTEST = True # 打开测试
#ISTEST = False # 关闭测试
if ISTEST:
    try:
        get_Grammar()
        with open('test.c')as f:
            contents = f.read()
            data = contents # 计算错误所在列数
        yacc.parse(contents)
        print(symTab.keys())
        if(error_num==0):
            print("grammar is true")
    except EOFError:
        print("Can't open file")
