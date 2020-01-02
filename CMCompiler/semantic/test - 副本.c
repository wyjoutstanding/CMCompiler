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
    //x = input();
    //y = input();
    //output(gcd(x, y));
    return;
}