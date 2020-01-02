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