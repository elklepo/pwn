/*
 * gcc one_time_pad.c -o one_time_pad
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

const char const flag[] = "flag{flagflagflagflagflagflag}";
int main()
{
    puts("here is your flag encrypted with one-time pad:");
    srand(time(NULL));
    for(size_t i=0; i < sizeof(flag); ++i)
    {
        printf("%02x", flag[i] ^ (rand() & 0xFF)); 
    }
    puts("\nhave fun, bye.");
}
