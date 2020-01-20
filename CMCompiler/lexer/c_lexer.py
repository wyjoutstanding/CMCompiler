# =============================================================================
# 文件名：c_lexer.py
# 功能：基于python-lex的C-词法分析器
# 作者： 常为， 荆顺吉
# 时间：2019/12/29
#==============================================================================
# *接口说明*
#   - getToken() : 获取下一个token
#   返回值：LexToken(str type, repr value, int lineno, int lexpos)
#         词法对象的参数依次为：类型，值，行号，在字符串中的偏移（从1开始）
#
# *如何使用*
#   - 作为模块使用时注释/关闭末尾的测试代码，调用getToken即可
#
# *有用参考*
#   - 英文文档：http://www.dabeaz.com/ply/ply.html （强烈推荐）
#   - 中文文档：https://www.cnblogs.com/P_Chou/p/python-lex-yacc.html
# =============================================================================
# *实现思路*impo

#   三步走：1.定义tokens 2.对每个token定义正则表达式 3.输入字符串，调用lex构建分析器
# =============================================================================

import ply.lex as lex # 导入python lex模块

# =============================================================================
# 1. tokens 列表定义
#   tokens必须要有，非终结符的命名都可以写在这
#   里面的每个符号都要有对应正则定义,且以 t_ 开头，详细见后文 
# =============================================================================
tokens = [
    #算数运算符
    'add', 'sub', 'mul', 'div',
    #关系运算符
    'less', 'greater', 'unequal', 'equal', 'notless', 'notgreater',
    #赋值运算符
    'assignment',
    #界符
    'bracel', 'bracer', 'parenl', 'parenr', 'bracketl', 'bracketr', 'comma', 'semi', 'annotation',
    #常量
    'NUMINT','NUMFLOAT',
    #标识符
    'ID',
    #换行符
    'LF',
    'tab'
]

# 关键字/保留字；本质上也可以写在tokens，但这里单独处理效率高
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'return' : 'RETURN',
    'void' : 'VOID',
    'while' : 'WHILE',
    'int' : 'INT',
    'float':'FLOAT'
}

# 将保留字添加到tokens，因为lex只识别关键字tokens
tokens += reserved.values()

# =============================================================================
# 2.以下为各个token的正则表达式定义，采用 t_tokenName 的命名方式
# 若要对其进行运算，可通过定义函数的方式
# =============================================================================

# 定义忽略字符的正则表达式，也可以通过定义相应函数不返回达到相同效果
# 比如下面的注释，换行，tab忽略
t_ignore = r'[ ]+'

# 关系、算术运算符
t_unequal = r'!='
t_notless = r'>='
t_notgreater = r'<='
t_equal   = r"=="

t_add   = r'\+'
t_sub   = r'-'
t_mul   = r'\*'
t_div   = r'/'
t_less    = r'<'
t_greater = r'>'
t_assignment = r'='

#界符
t_bracel    = r'{'
t_bracer    = r'}'
t_parenl    = r'\('
t_parenr    = r'\)'
t_bracketl  = r'\['
t_bracketr  = r'\]'
t_comma     = r','
t_semi      = r';'

#===================================================================
# 通过函数定义正则表达式，可以增加额外动作，比如给value重新赋值，或增加其余字段信息
#===================================================================
# 忽略注释
def t_annotation(t):
    r'(/\*(.|\n)*?\*/)|(\/\/.*)' # 第一行写正则表达式
    t.lexer.lineno += t.value.count('\n') # 累计行数
    pass # 表示忽略该token

# 忽略换行
def t_LF(t):
    r'[ ]+\n'
    pass

# 忽略tab
def t_tab(t):
    r'\t'
    pass

# 识别数字
def t_NUMINT(t):
    r'[0-9]+'
    t.value = int(t.value) # 返回时字符串类型，需转为整型
    return t

def t_NUMFLOAT(t):
    r'[0-9]*\.?[0-9]+$'
    t.value = float(t.value)  # 返回时字符串类型，需转为float型
    return t

#识别标识符
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# 增加行数
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) # 计算行数
    
# 错误处理：输出错误符号，行数，列数后跳过当前错误继续扫描
def t_error(t):
    #print("Illegal character '%s'" % t.value[0], "(%d," % t.lexer.lineno, "%d)" % t.lexer.lexpos)
    tmp = t.lexpos - data.rfind('\n',0,t.lexpos)
    print(f"========Illegal character: {t.value[0]}   line: {str(t.lineno)}   col: {str(tmp)}")
    t.lexer.skip(1) # 跳过当前字符

# =============================================================================
# 3.以下为测试输入与词法分析器构建部分
# =============================================================================

# 调用Lex模块，构建词法分析器
lexer = lex.lex()

# 测试输入文件与结果输出文件
f = open('test_input/testcase3/curTest.c', 'r', encoding='UTF-8')
f1 = open('output.txt', 'w')   #输出结果

data = f.read() # 获取输入串

lexer.input(data) # 将输入串输入词法分析器

# =============================================================================
# 测试部分：真正运行时将其注释掉 / 将ISTEST设为False
# =============================================================================
ISTEST = True # 打开测试
#ISTEST = False # 关闭测试
if ISTEST:
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
        tok = str(tok)
        f1.write(tok)
        f1.write("\n")

# =============================================================================
#  获取Token的接口
# =============================================================================
def getToken():
    return lexer.token()

# 文件流关闭
f.close()
f1.close()
