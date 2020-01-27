# CMCompiler说明文档

[toc]

## 实现功能

一个C语言子集编译器，基于PLY实现词法，语法分析，进而实现语义分析，语法制导翻译生成中间代码。文法定义在文末。

### 词法分析器

- [x] 识别合法单词种类，值
- [x] 去除无嵌套的多行注释`/* */`
- [x] 出错处理：给出错误字符，所在行数，列数；跳过当前字符继续扫描

### 语法分析器

- [x] 文法正确性判定
- [x] 出错处理:给出错误字符，所在行数;跳过错误字符继续扫描



## 如何运行

+ master为初级版本；**final分支为终极版本（完成所有功能）**

+ python>=3.0（推荐anaconda集成环境）
+ 克隆本项目，直接运行相应py脚本即可（**代码内有详细注释**）



## 目录结构

```c
├─CMCompiler 实现源码
│  ├─.spyproject  Spyder自动生成的项目文件，忽略它
│  ├─lexer	词法分析
│  │  └─test_input	测试输入文件
|  |  |_c_lexer.py	词法分析器实现
|  ├─grammar 语法分析
|  | ├─test.c 测试文件
|  | └─c_grammar.py 语法分析器实现
│  └─ply	PLY模块，从官网下载，不要轻易修改它
└─DesignDocument	设计文档
```



## 文法定义

### 词法集合

```
1.保留字/关键字
if else while int void return

2.运算符
+ - * / = 
< > 
== != <= >=

3.界符
( ) { } [ ] /* */

4.标识符
ID = '[a-zA-Z_][a-zA-Z_0-9]*'

5.常量（仅支持正整数）
Number = '[0-9]+'
```

### 语法定义

```
program -> declaration-list.
declaration-list -> declaration-list declaration | declaration
declaration -> var-declaration | fun-declaration
var-declaration -> type-specifier ID; | type-specifier ID [ NUM ];
type-specifier -> int | void
fun-declaration -> type-specifier ID ( params ) | compound-stmt
params -> params-list | void
params-list -> params-list, param | param
param -> type-specifier ID | type-specifier ID [ ]
compound-stmt -> { local-declarations statement-list }
local-declarations -> local-declarations var-declaration | empty
statement-list -> statement-list statement | empty
statement -> expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
expression-stmt -> expression ; | ;
selection-stmt -> if ( expression ) statement | if ( expression ) statement else statement
iteration-stmt -> while ( expression ) statement
return-stmt -> return ; | return expression;
expression -> var = expression | simple-expression
var -> ID | ID [ expression ]
simple-expression -> additive-expression relop additive-expression | additive-expression
relop -> <= | < | > | >= | == | !=
additive-expression -> additive-expression addop term | term
addop -> + | -
term -> term mulop factor | factor
mulop -> * | /
factor -> ( expression ) | var | call | NUM
call -> ID ( args )
args -> arg-list | empty
arg-list -> arg-list, expression | expression
```

