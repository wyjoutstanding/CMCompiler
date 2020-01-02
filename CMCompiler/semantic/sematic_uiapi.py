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
#def t_error(t):
#    global error_num
#    error_num += 1
#    #print("Illegal character '%s'" % t.value[0])
#    tmp = t.lexpos - data.rfind('\n',0,t.lexpos)
#    print(f"========Illegal character: {t.value[0]}   line: {str(t.lineno)}   col: {str(tmp)}")
#    #print("(%d," % t.lexer.lineno, "%d)" % t.lexer.lexpos)
#    t.lexer.skip(1)
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
    def __init__(self, _type=None, dataType=None, name=None, arrayLen=None, args=None, returnType=None):
        self._type = _type # ID类型，变量，数组，函数
        self.dataType = dataType # 变量和数组的数据类型
        self.name = name # ID名字
        self.arrayLen = arrayLen # 数组长度
        self.args = args # 函数参数列表
        self.returnType = returnType # 函数返回值类型
        
    def __str__(self): # 打印输出
        if self._type == 'var':
            ret = [('type',self._type), ('dataType', self.dataType), ('name', self.name)]
        elif self._type == 'array':
            ret = [('type',self._type), ('dataType', self.dataType), ('name', self.name), ('arrayLen', self.arrayLen)]
        else :
            ret = [('type',self._type), ('returnType', self.returnType), ('name', self.name), ('args', self.args)]
        return str(ret)
#a = SymTabItem(1,2,3)
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
#    for i in range(len(staticSymTab)-1, -1, -1):
#        t = staticSymTab[i]
#        if t.name == ID:
#            return t
    return None

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
    # 全局变量重定义检查
    item = existDef(staticSymTab, p[1].name)
#    print('item', item)
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
#    print(p[1]+" " +p[2])
#    symTab[p[2]] = SymTabItem(p[1], p[2])
#    item = existDef(staticSymTab, p[2])
#    print('item', item)
#    if item: # 重定义
#        errNoDefine('标识符',p[2],'重定义')
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
    p[0] = SymTabItem(_type='func', name=p[2], returnType=p[1], args=p[4])
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
#    print('p1', p[1])

def p_param_1(p):
    '''param : type_specifier ID'''
#    p[0] = p[2]
    p[0] = ['var',p[1],p[2]]
def p_param_2(p):
    '''param : type_specifier ID '[' ']' '''
#    p[0] = p[2]
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
#    print('item', item)
    if item: # 重定义
        errNoDefine('标识符',p[2].name,'重定义', -1) # 行号减一？？
    # 填入符号表
    funcSymTab.append(p[2])
#    print('local',p[2])
#    print("p2", p[2]._type, p[2].dataType, p[2].name)
def p_local_declarations_empty(p):
    '''local_declarations : '''
# 语句列表
def p_statement_list_1(p):
    '''statement_list : statement_list statement'''
    p[0] = p[1]
#    p[0].nextList += p[2].nextList
def p_statement_list_empty(p):
    '''statement_list : '''
    p[0] = Node('statement_list', 'state_list')
# 表达式；符合语句；选择；循环；返回
def p_statement_1(p):
    '''statement : expression_stmt'''
#    p[0] = Node('statement', 'name')
    p[0] = p[1]
def p_statement_2(p):
    '''statement : compound_stmt'''
#    p[0] = Node('statement', 'name')
    p[0] = p[1]
def p_statement_3(p):
    '''statement : selection_stmt'''
#    p[0] = Node('statement', 'name')
    p[0] = p[1]
def p_statement_4(p):
    '''statement : iteration_stmt'''
#    p[0] = Node('statement', 'name')
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
#    backPatch(p[1].nextList, p[3])
    p[0] = p[1]
def p_expression_stmt_2(p):
    '''expression_stmt : ';' '''
# IF语句
# N必须同时加，否则出现reduce/reduce冲突
def p_selection_stmt_1(p):
    '''selection_stmt : IF '(' expression ')' M statement N'''
    backPatch(p[3].trueList, p[5])
    p[0] = Node('selection_stmt', 'selec_stmt')
#    print('p6', p[3], p[6], p[5], p[7])
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
#    print('p0', p[0])
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
#    newLabel()
#    print("labelNum",labelNum, p[6],p[8])
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
#    p[1] = p[3] # 直接赋值
#    p[0] = Node('expression', tmp, children=[p[1],p[3]])
    p[0] = Node('expression', p[1].name, children=[p[1],p[3]])
def p_expression_2(p):
    '''expression : simple_expression'''
    p[0] = p[1]
#    print("==",p[0],p[1])
    
# 变量：普通变量或数组
def p_var_1(p):
    ''' var : ID'''
#    p[0] = p[1]
#    print('ID:',p[1])
    p[0] = Node('var', p[1])
    item = getID(p[1])
    if not item:
        errNoDefine('变量', p[1])
    elif item._type != 'var':
        if item._type == 'array':
            errNoDefine('变量', p[1], '已定义为 数组')
        else:
            errNoDefine('变量', p[1], '已定义为 函数，不可作为左值')
#        global error_num
#        error_num += 1
#        print('Error'+str(error_num)+'   行号:'+str(lex.lexer.lineno) + '   变量: 【'+p[1]+'】 未定义')
#    print('name',p[0].name)
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
    if p[3].ttype == 'NUM' and int(item.arrayLen) <= int(p[3].name):
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
#    p[0] = Node('simple_expression', p[1].name, children = [p[1]])
#    p[0].type = 'simple_expression'
#    p[0] = RelOpExpr('simple_expression', name=p[1].name)
#    p[0] = Node('simple_expression', name=p[1].name)
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
#    p[0] = Node('addop', p[1])
def p_addop_2(p):
    '''addop : '-' '''
    p[0] = p[1]
#    p[0] = Node('addop', p[1])

# 生成代码
def p_term_1(p):
    '''term : term mulop factor'''
    p[0] = newTmp() # 新建标号
#    print(newLabel(),': ',(p[2], p[1], p[3], p[0]))
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
#    p[0] = p[2]
    p[0] = Node('factor', p[2].name)
    
def p_factor_2(p):
    '''factor : var'''
#    p[0] = p[1]
    p[0] = Node('factor', p[1].name)
    
def p_factor_3(p):
    '''factor : call'''
    p[0] = Node('factor', p[1].name)
    
def p_factor_4(p):
    '''factor : NUM'''
#    p[0] = p[1]
    p[0] = Node('NUM', p[1])
#    print('factor : NUM', p[1])

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
        if not (p[3] != None and len(item.args) == len(p[3].name) or (item.args[0]=='VOID' and p[3]==None)):
#            for i in range(0, len(p[3].name)):
#                print('-------------itemargs',item.args,p[3].name)
#                if item.args[i][0] != p[3].name[0] and p[3].name[0] != 'factor':
#                    errNoDefine('函数参数类型不匹配',str(p[3].name[0]), str(item.args[i][0]))
                
        
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
#    print("p[0]",p[0].name, p[1].name, p[3].name)
#    p[0] = p[1] + p[3] # 拼接参数
#    p[0] = Node('arg_list', leaf=[p[1],p[2]])
#    print("arglist "+p[1],  "expression "+p[2], "p[0] " + p[0])
def p_arg_list_2(p):
    ''' arg_list : expression'''
    p[0] = p[1]
#    p[0].name = [p[0].name]
    p[0].name = [(p[1].ttype, p[0].name)]
#    p[0] = Node('arg_list',leaf=[p[1]])
#    print("expression"+p[1])

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
data = '' # 存储输入字符串
def setData(_data):
    global data
    data = _data
def getData():
    return data

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
            return 0
        #语法错误
        else:
            errorfile.close()
            return 1
    except EOFError:
        return 2




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
# 下一条四元式标号
def nextQuad():
    return labelNum+1
# 新建中间变量
def newTmp():
    global tmpNum
    tmpNum += 1
    return 'T'+str(tmpNum)
code = [0] # 存放代码
# 打印四元式:标号，操作符，参数1，参数2，结果
def printQtua(labelNum=None, op='_', arg1='_', arg2='_', result='_'):
    code.append([op, arg1, arg2, result])
#    print(str(labelNum)+') : ', (op, arg1, arg2, result))

def showQuad():
    with open("code.out","w", encoding='UTF-8') as f:
        f.write(str(len(code))+'\n')
        for i in range(1,len(code)):
#        print(quad)
#            f.write(str(i)+') : '+str(code[i])+'\n')
            f.write(str(code[i][0])+' '+ str(code[i][1])+' '+ str(code[i][2])+' ' +str(code[i][3])+'\n')
    for i in range(1,len(code)):
#        print(quad)
        print(str(i)+') : ', code[i])
# 回填
def backPatch(_list=[], quad=0):
    for i in _list:
        code[i][3] = quad
# AST节点
class Node:
    def __init__(self,_type,name,children=None,leaf=None):
        self.ttype = _type
        self.name = name
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf
        # 条件语句
        self.trueList = []
        self.falseList = []
        # S.nextList
        self.nextList = []
class RelOpExpr(Node):
    def __init__(self, _type, name,children=None, leaf=None, trueList=[], falseList=[]):
        Node.__init__(_type, name, children, leaf)
        self.trueList = trueList
        self.falseList = falseList
                
# =============================================================================
# 接口：运行时生成相应的parse.out和parsetab.py文件供之后使用
# =============================================================================
#import ply.yacc as yacc
#import ply as yacc
#import yacc_ui as yacc # 包含界面处理的yacc
def get_Grammar():
    yacc.yacc()

# =============================================================================
# 测试部分：真正运行时将其注释掉 / 将ISTEST设为False
# =============================================================================
ISTEST = False # 打开测试
#ISTEST = False # 关闭测试
if ISTEST:
    try:
        get_Grammar()
        with open('test1.c', encoding='UTF-8')as f:
            contents = f.read()
#            data = contents # 计算错误所在列数，测试时去除注释
        yacc.parse(contents)
        showQuad() # 打印四元式
#        print(symTab.keys())
        if(error_num==0):
            print("grammar is true")
    except EOFError:
        print("Can't open file")
