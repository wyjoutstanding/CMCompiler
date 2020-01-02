/*
    测试用例1：函数调用
*/
int x;
int a;
int array[8];
int fun(int b,int c, int m[]) {
    int a;
    while(a<1) {
        int aa;int dd;
        if (a < 2) x = 1; // 无else的分支；注释1
        x = 2;
        aa = 1; // 作用域检查
        b = 1; // 作用域检查
    /*    if (a < 1) x = 1;
        else x = 2;*/
        if (b == 0) { // 嵌套的条件分支测试
            int cc;
            if (x < 2) {
                int cc; // 作用域测试，变量声明只能写在’{‘最开始
                x =2;
            }
            else {
                x = 3;
            }
            return x;
        } 
        else {      
            return fun(b, b-b/c*c,a);
        }
        while(a > 10) { // 循环嵌套测试
            a = 0;
        }
    }

    return a+1;
}
void funvoid(void) {
    int x1;
    int x2[10];
    x = 1;
//    aa = 2;
//    x=array[8];
//    fun = 1; // 函数作左值测试
}
void main() {
    int mm;
//    funvoid(); // 空函数测试
//    x=2*fun(a,2); // 函数调用测试
    /*表达式，数组，四则运算，括号测试*/
   x = array[2-x]+x*2-(5-(12+a))/2-(a+2)/12*1; 
//   x = a[2-x]+x*2-(5-(12+a))/2-(a+2)/12*1; 
}