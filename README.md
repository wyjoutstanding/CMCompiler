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

  - [x] 变量定义：`int a`
  - [x] 函数定义：`void fun(prams)`（作用域问题）
  - [x] 一维数组定义：`int a[num]`

- 简单表达式：

  - [x] 括号，四则运算：`a-2*(2+1)/3`
  - [x] 一维数组引用：`a[3]-2`
  - [x] 函数调用：`fun(12)`（4元式直接跳转相应位置？？还是先记录在符号表？）
  - [x] 函数返回
+ 复杂语句
  - [x] 赋值
  - [x] 条件（有/无else；自嵌套/）
  - [x] 循环（自嵌套）

#### 类型检查

+ 作用域检查
  + 当前作用域重复定义变量
  + 变量使用前先声明
+ 函数调用参数个数，类型匹配；函数返回值检查

| （作用域）检查项目\ID类型 | 变量 | 数组     |                                |
| ------------------------- | ---- | -------- | ------------------------------ |
| 重定义/未定义             |      |          |                                |
|                           |      | 下标越界 | 返回值匹配，调用参数列表，左值 |
|                           |      |          |                                |



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

```
/* A program to perform Euclid s Algorithm to compute gcd.


 */
int gcd(int u, int v) {
    if (v == 0) {
        return u;
    } else {
        return gcd(v, u-u/v*v);
    }
    /* u-u/v*v* == u mod v */
}
void test(void){
    
}
void main() {
    int x;
    int y;
	 x = 2;
    x = input();
    y = input();
    output(gcd(x, y));
    return;
}
// 输出============
1) :  ['j==', 'v', '0', 3]
2) :  ['j', '_', '_', 5]
3) :  ['Return', 'u', '_', '_']
4) :  ['j', '_', '_', 12]
5) :  ['/', 'u', 'v', 'T2']
6) :  ['*', 'T2', 'v', 'T3']
7) :  ['-', 'u', 'T3', 'T4']
8) :  ['Param', 'v', '_', '_']
9) :  ['Param', 'T4', '_', '_']
10) :  ['Call', 'gcd', 2, 'T5']
11) :  ['Return', 'T5', '_', '_']
12) :  ['=', '2', '_', 'x']
13) :  ['Call', 'input', 0, 'T6']
14) :  ['=', 'T6', '_', 'x']
15) :  ['Call', 'input', 0, 'T7']
16) :  ['=', 'T7', '_', 'y']
17) :  ['Param', 'x', '_', '_']
18) :  ['Param', 'y', '_', '_']
19) :  ['Call', 'gcd', 2, 'T8']
20) :  ['Param', 'T8', '_', '_']
21) :  ['Call', 'output', 1, 'T9']
22) :  ['Return', '_', '_', '_']
```

+ 分支，循环，数组/函数引用，表达式

```
/*
    测试用例1：函数调用
*/
int x;
int a;

int fun(int b,int c) {
    while(a<1) {
        if (a < 2) x = 1; // 无else的分支；注释1
        x= 2;
    /*    if (a < 1) x = 1;
        else x = 2;*/
        if (v == 0) { // 嵌套的条件分支测试
            if (x < 2) {
                x =2;
            }
            else {
                x = 3;
            }
            return u;
        } 
        else {      
            return gcd(v, u-u/v*v);
        }
        while(a > 10) { // 循环嵌套测试
            a = 0;
        }
    }

    return a+1;
}
void funvoid(void) {

}
void main() {
    funvoid(); // 空函数测试
    x=2*fun(a,2); // 函数调用测试
    /*表达式，数组，四则运算，括号测试*/
   x = a[2-x]+x*2-(5-(12+a))/2-(a+2)/12*1; 
}
// 输出================
1) :  ['j<', 'a', '1', 3]
2) :  ['j', '_', '_', 28]
3) :  ['j<', 'a', '2', 5]
4) :  ['j', '_', '_', 6]
5) :  ['=', '1', '_', 'x']
6) :  ['=', '2', '_', 'x']
7) :  ['j==', 'v', '0', 9]
8) :  ['j', '_', '_', 16]
9) :  ['j<', 'x', '2', 11]
10) :  ['j', '_', '_', 13]
11) :  ['=', '2', '_', 'x']
12) :  ['j', '_', '_', 14]
13) :  ['=', '3', '_', 'x']
14) :  ['Return', 'u', '_', '_']
15) :  ['j', '_', '_', 23]
16) :  ['/', 'u', 'v', 'T5']
17) :  ['*', 'T5', 'v', 'T6']
18) :  ['-', 'u', 'T6', 'T7']
19) :  ['Param', 'v', '_', '_']
20) :  ['Param', 'T7', '_', '_']
21) :  ['Call', 'gcd', 2, 'T8']
22) :  ['Return', 'T8', '_', '_']
23) :  ['j>', 'a', '10', 25]
24) :  ['j', '_', '_', 27]
25) :  ['=', '0', '_', 'a']
26) :  ['j', '_', '_', 23]
27) :  ['j', '_', '_', 1]
28) :  ['+', 'a', '1', 'T10']
29) :  ['Return', 'T10', '_', '_']
30) :  ['Call', 'funvoid', 0, 'T11']
31) :  ['Param', 'a', '_', '_']
32) :  ['Param', '2', '_', '_']
33) :  ['Call', 'fun', 2, 'T12']
34) :  ['*', '2', 'T12', 'T13']
35) :  ['=', 'T13', '_', 'x']
36) :  ['-', '2', 'x', 'T14']
37) :  ['*', 'T14', '4', 'T15']
38) :  ['[]', 'a', 'T15', 'T16']
39) :  ['*', 'x', '2', 'T17']
40) :  ['+', 'T16', 'T17', 'T18']
41) :  ['+', '12', 'a', 'T19']
42) :  ['-', '5', 'T19', 'T20']
43) :  ['/', 'T20', '2', 'T21']
44) :  ['-', 'T18', 'T21', 'T22']
45) :  ['+', 'a', '2', 'T23']
46) :  ['/', 'T23', '12', 'T24']
47) :  ['*', 'T24', '1', 'T25']
48) :  ['-', 'T22', 'T25', 'T26']
49) :  ['=', 'T26', '_', 'x']
```

