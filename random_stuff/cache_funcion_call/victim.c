#include <stdio.h>
#include <unistd.h>

long long int foo(long long int a, long long int *b)
{
    sleep(2);
    printf("called with args: %lld, %lld\n", a, *b);
    a += *b;
    *b = (*b + 1) % 2;
    return a;
}

int main()
{
    long long int a, b, b_ref, r;

    a = 7;
    b = 1;
    b_ref = b;
    r = foo(a, &b);
    printf("%lld, %lld -> %lld, %lld\n", a, b_ref, r, b);

    a = 7;
    b = 0;
    b_ref = b;
    r = foo(a, &b);
    printf("%lld, %lld -> %lld, %lld\n", a, b_ref, r, b);

    a = 7;
    b = 1;
    b_ref = b;
    r = foo(a, &b);
    printf("%lld, %lld -> %lld, %lld\n", a, b_ref, r, b);

    a = 5;
    b = 1;
    b_ref = b;
    r = foo(a, &b);
    printf("%lld, %lld -> %lld, %lld\n", a, b_ref, r, b);

    a = 7;
    b = 0;
    b_ref = b;
    r = foo(a, &b);
    printf("%lld, %lld -> %lld, %lld\n", a, b_ref, r, b);
    
    a = 5;
    b = 1;
    b_ref = b;
    r = foo(a, &b);
    printf("%lld, %lld -> %lld, %lld\n", a, b_ref, r, b);

    a = 5;
    b = 1;
    b_ref = b;
    r = foo(a, &b);
    printf("%lld, %lld -> %lld, %lld\n", a, b_ref, r, b);

}

