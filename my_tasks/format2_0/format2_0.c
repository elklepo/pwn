/*
 * clang format2_0.c -m32 -O0 -Wl,-z,relro -fstack-protector -fPIC -pie -o format2_0
*/

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

typedef unsigned int uint;

char buff[128];

void flag()
{
    char flag[33] = { 0 };
    int fd = open("./flag", O_RDONLY);
    read(fd, flag, 32);
    puts(flag);
}

void foo(int a, int b, int c, int **ppx, int d, int **ppy)
{
    printf("%p\n%p\n", (uint)*ppx + a * c, (uint)flag - b * d);
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
    
    foo(0xf00d, 0x1337, 0xbad, &s.px, 0x997, &s.py);

    read(0, buff, sizeof(buff));
    
    printf(buff);
    
    exit(0);
}
