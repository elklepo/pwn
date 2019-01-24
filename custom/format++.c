/*
 * clang format++.c -m32 -O0 -Wl,-z,relro -fstack-protector -fPIC -pie -o format++
*/

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

char buff[256];

void print_flag()
{
    char flag[33] = { 0 };
    int fd = open("./flag", O_RDONLY);
    read(fd, flag, 32);
    puts(flag);
}

void foo(int a, int **ppx, int b, int **ppy)
{
    printf("%x\n%x\n", **ppx + a * b, print_flag - a * b);
}

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0); 

    struct
    {
        int *px;
        int  x;
        int *py;
        int  y;
    }s; 
    
    s.px = &s.x;
    s.x  = 0xdeadface;
    s.py = &s.y;
    s.y  = 0xcafebabe;

    read(0, buff, sizeof(buff));
    
    foo(1337, &s.px, 997, &s.py);

    printf(buff);
    
    exit(0);
}
