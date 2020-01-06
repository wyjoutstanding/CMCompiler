# =============================================================================
# 文件名：c_grammar.py
# 功能：基于python-lex和python-yacc的C-语法分析器
# 作者： 武起龙，张峥
# 时间：2019/12/29
#==============================================================================
# *接口说明*
#   - getGrammar() : 生成parsetab.py和parse.out文件
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
errorfile = None # 错误文件
parser = 0 # lexer
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
    global errorfile
    if(errorfile is None):
        errorfile = open("error.out",'w',encoding='UTF-8')
    tmp = t.lexpos - getData().rfind('\n',0,t.lexpos)
    errorfile.write("LEX : Illegal character : "+t.value[0]+"    line :"+str(t.lexer.lineno)+  '  col: '+str(tmp)+'\n')
    error_num+=1
    t.lexer.skip(1)
import ply.lex as lex # 导入python lex模块

#lex.lex()# 调用Lex模块，构建词法分析器

# =============================================================================
# 符号表
# =============================================================================
class SymTabItem:
    def __init__(self, _type=None, dataType=None, name=None, arrayLen=None, args=None, returnType=None, codeNum=0):
        self._type = _type # ID类型，变量，数组，函数
        self.dataType = dataType # 变量和数组的数据类型
        self.name = name # ID名字
        self.arrayLen = arrayLen # 数组长度
        self.args = args # 函数参数列表
        self.returnType = returnType # 函数返回值类型
        self.codeNum = codeNum # 四元式开始的位置
        
    def __str__(self): # 打印输出
        if self._type == 'var':
            ret = [('type',self._type), ('dataType', self.dataType), ('name', self.name)]
        elif self._type == 'array':
            ret = [('type',self._type), ('dataType', self.dataType), ('name', self.name), ('arrayLen', self.arrayLen)]
        else :
            ret = [('type',self._type), ('returnType', self.returnType), ('name', self.name), ('args', self.args), ('codeNum', self.codeNum)]
        return str(ret)
staticSymTab = dict() # 全局符号表，存放静态声明的变量，数组，函数
funcSymTab = [] # 过程的符号表，不同作用域以$分割

# =============================================================================
# 根据ID查询符号表，存在则返回相应表项，否则返回None
# 先从当前过程的符号表开始逆序查询，找到第一个立即返回；若当前表不存在，到全局静态区继续找
# =============================================================================
def getID(ID):
    for i in range(len(funcSymTab)-1, -1, -1):
        t = funcSymTab[i]
        if t != '$' and t.name == ID:
            return t
    if staticSymTab.get(ID):
        return staticSymTab[ID]
    return None

# 错误处理输出模板
def errNoDefine(messType, IDName, mess2='未定义',lineNo=0):
    global error_num
    error_num += 1
    global errorfile
    if(errorfile is None):
        errorfile = open("error.out",'w',encoding='UTF-8')
    errorfile.write('Sematic : Error'+str(error_num)+'   line:'+str(lex.lexer.lineno+lineNo) + '   '+str(messType)+': 【'+str(IDName)+'】'+ str(mess2)+'\n')
    print('Error'+str(error_num)+'   行号:'+str(lex.lexer.lineno+lineNo) + '   '+messType+': 【'+IDName+'】'+ mess2)

# 判断ID在当前作用域是否已定义，若是，返回相应item，否则返回空
def existDef(table=[], ID=None):
    if type(table) == dict:
        print('dict',table.get(ID))
        return table.get(ID)
    for i in range(len(table)-1,-1,-1):
        if table[i] == '$':
            return None
        if table[i].name == ID:
            return table[i]
    return None

#==============================================================================
#产生式列表-语法分析过程中夹杂着语义分析（每个产生式下方插入的为语义动作）
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
    # 全局变量重定义检查
    item = existDef(staticSymTab, p[1].name)
    if item: # 重定义
        errNoDefine('标识符',p[1].name,'重定义',lineNo=-1) # 行号多一行？
        
    staticSymTab[p[1].name] = p[1] # 全局静态符号表    
    print('---staticVar----',p[1])
def p_declaration_2(p):
    '''declaration : fun_declaration'''
    if p[1]:
        staticSymTab[p[1].name] = p[1] # 全局静态符号表    
        print('----staticfunc----',p[1])
    
# 变量声明具体定义：普通变量；一维数组
def p_var_declaration_1(p):
    '''var_declaration : type_specifier ID ';' '''
    p[0] = SymTabItem(_type='var', dataType=p[1], name=p[2])
        
def p_var_declaration_2(p):
    '''var_declaration : type_specifier ID '[' NUM ']' ';' '''
    p[0] = SymTabItem(_type='array', dataType=p[1], name=p[2], arrayLen=p[4])
# 变量/函数声明类型：INT;VOID
def p_type_specifier_1(p):
    '''type_specifier : INT'''
    p[0] = 'INT'
def p_type_specifier_2(p):
    '''type_specifier : VOID'''
    p[0] = 'VOID'

# 函数声明：头部；过程体
def p_fun_declaration_1(p):
    '''fun_declaration : type_specifier ID '(' params ')' '''
    p[0] = SymTabItem(_type='func', name=p[2], returnType=p[1], args=p[4], codeNum=nextQuad())
    funcSymTab.append('$')
    if p[4] and p[4][0] != '$' and p[4][0] != 'VOID':
        for arg in p[4]: #保存函数形式参数与当前作用域
            funcSymTab.append(SymTabItem(_type=arg[0], dataType=arg[1], name=arg[2]))
#            print('arg',arg)
def p_fun_declaration_2(p):
    '''fun_declaration : compound_stmt'''
    print('****')
    for i in funcSymTab:
        if i != '$':
            print('fd==',i)
    funcSymTab.clear() # 函数结束，清空当前过程的符号表

#def p_E1(p): # 记录函数声明
#    '''E1 : '''
#    
# 参数定义:二维数组存放[[type,dataType,name],[]]
def p_params_1(p):
    '''params : param_list'''
    p[0] = p[1]
def p_params_2(p):
    '''params : VOID'''
    p[0] = ['VOID']
def p_params_empty(p):
    '''params : '''
    
def p_param_list_1(p):
    '''param_list : param_list ',' param'''
    p[1].append(p[3]) # 不可直接赋值，append无返回值
    p[0] = p[1]
#    print('p1list', p[1], p[0])
def p_param_list_2(p):
    '''param_list : param'''
    p[0] = [p[1]]

def p_param_1(p):
    '''param : type_specifier ID'''
    p[0] = ['var',p[1],p[2]]
def p_param_2(p):
    '''param : type_specifier ID '[' ']' '''
    p[0] = ['array',p[1],p[2]]

# 函数体
def p_compound_stmt_1(p):
    '''compound_stmt : '{' E1 local_declarations statement_list '}' '''
#    '''compound_stmt : '{' local_declarations statement_list '}' '''
    p[0] = p[4]
    l = len(funcSymTab)
    for i in range(l-1, -1, -1): # 逆序查找，直到$出现，删除这之间所有变量（模拟栈）
        print('          ---localFunc[i]',funcSymTab[i])
        if funcSymTab[i] == '$':
            funcSymTab.pop()
            break
        else:
            funcSymTab.pop()
            
def p_E1(p): # 作用域控制标记，{}
    ''' E1 : '''
    funcSymTab.append('$')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$')
def p_local_declarations_1(p):
    '''local_declarations : local_declarations var_declaration'''
    # 局部变量重定义检查
    item = existDef(funcSymTab, p[2].name)
    if item: # 重定义
        errNoDefine('标识符',p[2].name,'重定义', -1) # 行号减一？？
    # 填入符号表
    funcSymTab.append(p[2])
def p_local_declarations_empty(p):
    '''local_declarations : '''
# 语句列表
def p_statement_list_1(p):
    '''statement_list : statement_list statement'''
    p[0] = p[1]
def p_statement_list_empty(p):
    '''statement_list : '''
    p[0] = Node('statement_list', 'state_list')
# 表达式；符合语句；选择；循环；返回
def p_statement_1(p):
    '''statement : expression_stmt'''
    p[0] = p[1]
def p_statement_2(p):
    '''statement : compound_stmt'''
    p[0] = p[1]
def p_statement_3(p):
    '''statement : selection_stmt'''
    p[0] = p[1]
def p_statement_4(p):
    '''statement : iteration_stmt'''
    p[0] = p[1]
def p_statement_5(p):
    '''statement : return_stmt'''
    p[0] = p[1]
    if p[1] == 'VOID':
        printQtua(newLabel(), 'Return', '_', '_', '_')
    else:
        printQtua(newLabel(), 'Return', p[1].name, '_', '_')
    p[0] = Node('statement', 'name')
        

# 表达式语句
def p_expression_stmt_1(p):
    '''expression_stmt : expression ';' '''
    p[0] = p[1]
def p_expression_stmt_2(p):
    '''expression_stmt : ';' '''
# IF语句
# N必须同时加，否则出现reduce/reduce冲突
def p_selection_stmt_1(p):
    '''selection_stmt : IF '(' expression ')' M statement N'''
    backPatch(p[3].trueList, p[5])
    p[0] = Node('selection_stmt', 'selec_stmt')
    code.pop() # 删除N推入多余的记录
    global labelNum
    labelNum -= 1 # 标号位置也要回退1
    p[0].nextList = p[3].falseList + p[6].nextList
    backPatch(p[0].nextList, p[7][0])
#    backPatch(p[3].falseList, p[4])
# 第三个M用来回填nextList，即跳过S2
def p_selection_stmt_2(p):
    '''selection_stmt : IF '(' expression ')' M statement N ELSE M statement M'''
    backPatch(p[3].trueList, p[5])
    backPatch(p[3].falseList, p[9])
    p[0] = Node('selection_stmt_2', 'selec_stmt_2')
    # S.nextList = merge(S1.nextList+N.nextList+S2.nextList)
    p[0].nextList = p[6].nextList+ p[7] + p[10].nextList
    backPatch(p[0].nextList, p[11])
# 增加空产生式，作为标记
def p_M(p): # 下一个语句开始
    '''M :'''
    p[0] = nextQuad()
def p_N(p): # 无条件跳转
    '''N :'''
    p[0] = [nextQuad()] # N.nextlist = makeList(nextquad)
    printQtua(newLabel(), 'j')
    
# WHILE语句:增加两个M标号
def p_iteration_stmt_1(p):
    '''iteration_stmt : WHILE M '(' expression ')' M statement M'''
    backPatch(p[7].nextList, p[2])
    backPatch(p[4].trueList, p[6])
    p[0] = Node('while', 'while')
    p[0].nextList = p[4].falseList
    printQtua(newLabel(), 'j', result=p[2])
    backPatch(p[0].nextList, p[8]+1) # 增加一条while最后无条件跳转

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
    tmp = newLabel()
    printQtua(tmp, p[2], p[3].name, '_', p[1].name) # 先产生代码
    p[0] = Node('expression', p[1].name, children=[p[1],p[3]])
def p_expression_2(p):
    '''expression : simple_expression'''
    p[0] = p[1]
    
# 变量：普通变量或数组
def p_var_1(p):
    ''' var : ID'''
    p[0] = Node('var', p[1])
    item = getID(p[1])
    if not item:
        errNoDefine('变量', p[1])
    elif item._type != 'var':
        if item._type == 'array':
            errNoDefine('变量', p[1], '已定义为 数组')
        else:
            errNoDefine('变量', p[1], '已定义为 函数，不可作为左值')

# 一维数组引用：a[m] => T = a[m*dataType.width]，[]中填偏移量
def p_var_2(p):
    ''' var : ID '[' expression ']' '''
    tmp1 = newTmp()
    printQtua(newLabel(), '*', p[3].name, '4', tmp1) # 偏移：T1 = expression.val * 4
    tmp2 = newTmp()
    p[0] = tmp2 # 其实并不需要记录tmp2的标号内有什么，只要记住他的索引即可
    printQtua(newLabel(), '[]', p[1], tmp1, tmp2) # 引用：T2 = ID[T1]
    # 建树
    p[0] = Node('var', tmp2)
    
    # 检查数组是否定义，是否越界
    item = getID(p[1])
    if not item:
        errNoDefine('数组', p[1])
    elif item._type != 'array':
        errNoDefine('变量', p[1], '不是数组类型')
    elif p[3].ttype == 'NUM' and int(item.arrayLen) <= int(p[3].name):
        errNoDefine('数组', p[1], '下标越界'+' 最大长度:'+str(item.arrayLen))
        
#=====================================
# 以下为表达式定义：优先级：关系符 < 加减 < 乘除
# 简单表达式：关系表达式
def p_simple_expression_1(p):
    '''simple_expression : additive_expression relop additive_expression'''
#    p[0] = RelOpExpr('simple_expression', newTmp(), children=[p[1],p[3]])
    p[0] = Node('simple_expression', newTmp(), children=[p[1],p[3]])
    p[0].trueList.append(nextQuad())
    p[0].falseList.append(nextQuad()+1)
    printQtua(newLabel(), 'j'+p[2], p[1].name, p[3].name, 0)
    printQtua(newLabel(), 'j', '_', '_', 0)
    
def p_simple_expression_2(p):
    '''simple_expression : additive_expression'''
    p[0] = p[1]

# 6种关系符号
def p_relop_1(p):
    '''relop : LE'''
    p[0] = p[1]
def p_relop_2(p):
    '''relop : '<' '''
    p[0] = p[1]
def p_relop_3(p):
    '''relop : '>' '''
    p[0] = p[1]
def p_relop_4(p):
    '''relop : GE'''
    p[0] = p[1]
def p_relop_5(p):
    '''relop : EE'''
    p[0] = p[1]
def p_relop_6(p):
    '''relop : NE'''
    p[0] = p[1]

# 四则运算：已考虑四则运算优先级
def p_additive_expression_1(p):
    '''additive_expression : additive_expression addop term'''
    p[0] = newTmp()
    printQtua(newLabel(), p[2], p[1].name, p[3].name, p[0])
    p[0] = Node('additive_expression', p[0], children=[p[1],p[3]])
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
    printQtua(newLabel(), p[2], p[1].name, p[3].name, p[0])
    p[0] = Node('term', p[0], children=[p[1],p[3]])
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
    p[0] = Node('factor', p[2].name)
    
def p_factor_2(p):
    '''factor : var'''
    p[0] = Node('factor', p[1].name)
    
def p_factor_3(p):
    '''factor : call'''
    p[0] = Node('factor', p[1].name)
    
def p_factor_4(p):
    '''factor : NUM'''
    p[0] = Node('NUM', p[1])

# 调用函数
def p_call_1(p):
    ''' call : ID '(' args ')' '''
    if p[3]: # 存在实参    
        for arg in p[3].name: # 遍历实参，生成param代码
            printQtua(newLabel(), 'Param', arg[1], '_', '_')
    tmpLabel = newTmp()
    plen = 0 # 参数个数
    if p[3]: # 处理无参情况
        plen = len(p[3].name)
    printQtua(newLabel(), 'Call', p[1], plen, tmpLabel) # 需输出函数名和参数个数
    # 建树
    p[0] = Node('call', tmpLabel)
    # 参数个数检查与类型检查
    item = getID(p[1])
    if not item: # 函数未定义
        errNoDefine('函数', p[1])
    else:
        # 个数检查
        if not (p[3] != None and item.args != None and len(item.args) == len(p[3].name) or (item.args != None and item.args[0]=='VOID' and p[3]==None)):
            errNoDefine('函数参数个数不一致', '_','_')
def p_args_1(p):
    '''args : arg_list'''
    p[0] = p[1]
def p_args_empty(p):
    '''args : '''
# 实参拼接
def p_arg_list_1(p):
    ''' arg_list : arg_list ',' expression'''
    p[1].name.append((p[3].ttype, p[3].name))
    p[0] = Node('arg_list', name=p[1].name)
def p_arg_list_2(p):
    ''' arg_list : expression'''
    p[0] = p[1]
    p[0].name = [(p[1].ttype, p[0].name)]

#错误处理，输出错误所在单词

def p_error(p):
    global error_num
    global errorfile
    global parser
    if(errorfile is None):
        errorfile = open("error.out",'w',encoding='UTF-8')
    if p :
        parser.errok()
        errorfile.write("Syntax :  error at `" + p.value+"`   line : "+str(p.lineno)+
                        '\nSkip this token and Step into Normal Mode\n')
    else:
        errorfile.write("Syntax : error at EOF \n")
    error_num+=1

import yacc_ui as yacc
#import ply.yacc_ui as yacc
# 对输出字符串的获取与设置
data = '' # 存储输入字符串
def setData(_data):
    global data
    data = _data
def getData():
    return data
# =============================================================================
# 初始化全局变量
# =============================================================================
def init():
    global staticSymTab
    staticSymTab.clear()
    global funcSymTab
    funcSymTab.clear()
    global labelNum
    labelNum = 0
    global tmpNum
    tmpNum = 0
    global code
    code = [0]

# =============================================================================
# 语法/语义分析接口，主要给ui界面调用
# 输入：file：文件名
# 返回：0：语法正确； 1：语法错误； 2：文件错误
# =============================================================================
def Analysis(file):
    init()
    lexer = lex.lex()# 调用Lex模块，构建词法分析器
    global parser
    global errorfile
    global error_num
    errorfile = None
    error_num = 0
    parser = yacc.yacc()
    try:
        with open(file, encoding='UTF-8')as f:
            contents = f.read()
#            data = contents # 词法错误列号处理
            setData(contents)
        parser.parse(contents,debug=1)
        #语法正确
        if(error_num==0):
            showQuad()
            global code
            outputASM(tranToAsm(code))
            return 0
        #语法错误
        else:
            errorfile.close()
            return 1
    except EOFError:
        return 2


# =============================================================================
# 一遍扫描的回填实现；抽象语法树的建立
# 四元式的标号，中间变量控制
# =============================================================================
labelNum = 0 # 四元式标号记录
tmpNum = 0 # 中间变量数量累计

# 新建标号
def newLabel():
    global labelNum
    labelNum += 1
    return labelNum
# 下一条四元式标号
def nextQuad():
    return labelNum+1
# 新建中间变量
def newTmp():
    global tmpNum
    tmpNum += 1
    return 'T'+str(tmpNum)
code = [0] # 存放四元式代码

# 打印四元式:标号，操作符，参数1，参数2，结果
def printQtua(labelNum=None, op='_', arg1='_', arg2='_', result='_'):
    code.append([op, arg1, arg2, result])
# 显示四元式，写到文件，同时打印控制台
def showQuad():
    with open("code.out","w", encoding='UTF-8') as f:
        f.write(str(len(code))+'\n')
        for i in range(1,len(code)):
            f.write(str(code[i][0])+' '+ str(code[i][1])+' '+ str(code[i][2])+' ' +str(code[i][3])+'\n')
    for i in range(1,len(code)):
        print(str(i)+') : ', code[i])

# 翻译if-then-else 和 while时的回填函数
def backPatch(_list=[], quad=0):
    for i in _list:
        code[i][3] = quad
        
# AST节点
class Node:
    def __init__(self,_type,name,children=None,leaf=None):
        self.ttype = _type # 类型
        self.name = name # 名字
        if children: # 孩子
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf # 叶子结点
        # 条件语句
        self.trueList = []
        self.falseList = []
        # S.nextList：语句
        self.nextList = []

# =============================================================================
# 四元式转换为汇编代码          
# =============================================================================
# 返回基本块标签，函数标签位置
def getLabelDict():    
    labelDict = {} # 记录需要表示的跳转标签，jmp,jrop,
    funcDict={} # 函数标签；call
    for c in code:
        if c != 0:
            if c[0][0] == 'j': # 有条件/无条件跳转
#                print('j',c)
                labelDict[c[3]] = '$Label'+str(c[3]) # 生成跳转标签
    for item in staticSymTab.keys():
        tmp = staticSymTab.get(item)
        if tmp._type == 'func':
            funcDict[tmp.codeNum] = tmp.name
    return labelDict, funcDict
# 关系符映射
relopDict = {
        'j<': 'JL',
        'j>': 'JG',
        'j>=': 'JGE',
        'j<=': 'JLE',
        'j==': 'JE',
        'j!=': 'JNE'
        }
# 二元算术转换，即四则运算
def binop(code=[], asmCode=[], op='+'):
    if code == []:
        return asmCode
    asm = 'MOV EAX, '+ code[1]
    asmCode.append(asm)
    asm = 'MOV EBX, '+ code[2]
    asmCode.append(asm)
    asm = op+' EAX, EBX'
    asmCode.append(asm)
    asm = 'MOV '+code[3]+', EAX'
    asmCode.append(asm)
    return asmCode
# 将四元式转换为汇编代码；
# quadCode为四元式列表；返回值为转换后的汇编代码列表
def tranToAsm(quadCode):
    labelDict , funcDict = getLabelDict()
    asmCode = []
    i = 0
    for code in quadCode:
        if code == 0:
            continue
        asm = ''
        i += 1
        # 函数或跳转标签存在，先打印
        funLabel = funcDict.get(i)
        label = labelDict.get(i)
        if funLabel != None:
            asmCode.append(funLabel+':')
        if label != None:
            asmCode.append(label+':')
#        print(code)
        # 继续处理四元式，根据动作类型进入不同处理
        if code[0][0] == 'j':
            if code[0] == 'j': # 无条件跳转
                asm = 'JMP '+labelDict[code[3]] # 无条件跳转
                asmCode.append(asm)
            else: # 分情况跳转
                # 先产生cmp，然后根据flag跳转
                asm = 'CMP '+ code[1]+' ,'+code[2]
                asmCode.append(asm)
                asm = relopDict[code[0]]+' '+labelDict[code[3]]
                asmCode.append(asm)
        # 参数压栈：PUSH、EAX
        elif code[0] == 'Param':
            asm = 'MOV EAX, '+ code[1]
            asmCode.append(asm)
            asm = 'PUSH EAX'
            asmCode.append(asm)
        # 调用函数
        elif code[0] == 'Call':
            asm = 'CALL '+code[1]
            asmCode.append(asm)
        # 函数返回
        elif code[0] == 'Return':
            asm = 'RET\n'
            asmCode.append(asm)
        elif code[0] == '+':
            asmCode = binop(code, asmCode, 'ADD')
        elif code[0] == '-':
            asmCode = binop(code, asmCode, 'SUB')
        elif code[0] == '/':
            asmCode = binop(code, asmCode, 'DIV')
        elif code[0] == '*':
            asmCode = binop(code, asmCode, 'MUL')
        # 赋值语句
        elif code[0] == '=':
            asm = 'MOV EAX, '+code[1]
            asmCode.append(asm)
            asm = 'MOV '+code[3]+', EAX'
            asmCode.append(asm)
        # 数组引用求值
        elif code[0] == '[]':
            asm = "MOV EBX, "+ code[1]
            asmCode.append(asm)
            asm = 'MOV ECX, ' + code[2]
            asmCode.append(asm)
            asm =  'MOV EDX, ' + '[EBX + ECX*4]'
            asmCode.append(asm)
            asm = 'MOV '+code[3]+', EDX'
            asmCode.append(asm)
    return asmCode

# 输出汇编头部信息，代码，数据段
# asmCode：汇编代码列表； fileName：输出的文件名
def outputASM(asmCode, fileName='output.asm'):
    with open(fileName, 'w', encoding='utf-8') as f: # 打开文件
        f.write('org 100H\n') # 起始偏移
        # 数据段
        f.write('\nSECTION data\n') 
        for key in staticSymTab.keys():
            var = staticSymTab.get(key)
            if var._type == 'var':
                f.write('\t'+var.name+' dd 0\n') # 初始化变量
            elif var._type == 'array': # 数组初始化
                f.write('\t'+var.name+' times '+ str(var.arrayLen) +' dd 0\n')
        f.write('\tT'+' times '+ str(len(code)) +' dd 0\n')
        # 代码段
        f.write('\nSECTION code\n') 
        f.write('\tMOV EAX, CS\n')
        f.write('\tMOV ESP, EAX\n') # 堆栈设置
        for asm in asmCode:
            if asm != 0:
                if asm.find(':') != -1:
                    f.write(asm+'\n')
                else:
                    f.write('\t'+asm+'\n')
# =============================================================================
# 接口：运行时生成相应的parse.out和parsetab.py文件供之后使用
# =============================================================================
#import yacc_ui as yacc # 包含界面处理的yacc
def get_Grammar():
    yacc.yacc()

# =============================================================================
# 测试部分：真正运行时将其注释掉 / 将ISTEST设为False
# =============================================================================
if __name__ == '__main__':
    ISTEST = True # 打开测试
    if ISTEST:
        ret = Analysis('./test_input/test_完全正确.c')
        if ret == 0:
            print('程序正确')
        else:
            print('出现错误')
        asmCode = tranToAsm(code)
        outputASM(asmCode)