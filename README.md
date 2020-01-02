# CMCompiler说明文档

[TOC]

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
fun-declaration -> type-specifier ID ( params ) compound-stmt // ！！注意这里|去除了
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



## 语义分析-翻译模式生成四元式

### 四元式

简单表达式，=》赋值=》

#### 表达式

- 说明语句：

  - [ ] 变量定义：`int a`
  - [ ] 函数定义：`void fun(prams)`（作用域问题）
  - [ ] 一维数组定义：`int a[num]`

- 简单表达式：

  - [x] 括号，四则运算：`a-2*(2+1)/3`
  - [x] 一维数组引用：`a[3]-2`
  - [x] 函数调用：`fun(12)`（4元式直接跳转相应位置？？还是先记录在符号表？）
  - [x] 函数返回
+ 复杂语句
  - [x] 赋值
  - [x] 条件（可嵌套）
  - [x] 循环（可嵌套）



### 测试

```
// 变量定义，括号，四则运算表达式，赋值语句测试
int x;
void main() {
   x = a-(5-(12+a))/2-(a+2)/12*1;
} 
// 输出
1) :  ('+', '12', 'a', 'T1')
2) :  ('-', '5', 'T1', 'T2')
3) :  ('/', 'T2', '2', 'T3')
4) :  ('-', 'a', 'T3', 'T4')
5) :  ('+', 'a', '2', 'T5')
6) :  ('/', 'T5', '12', 'T6')
7) :  ('*', 'T6', '1', 'T7')
8) :  ('-', 'T4', 'T7', 'T8')
9) :  ('=', 'T8', '_', 'x')
```

