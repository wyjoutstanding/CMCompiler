/* A program to perform Euclid's
Algorithm to compute gcd. */
test=1;
/* u-u/v*v == u mod v */
int gcd (int u, int v)
{  if (v == 0) return u ;
else return gcd(v,u-u/v*v);
/* u-u/v*v == u mod v */
}
void main(void)
{  int x; int y;
x = input(); y = input();
output ( gcd ( x , y  ) ) ;
}
