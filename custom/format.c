#include <string.h>
#include <stdio.h>
#include <unistd.h>

/**
gcc -o format format.c -m32  -fstack-protector-all -static
*/

char g_buffer[1024];

void age()
{
        char age[8];
        read(0, age, sizeof(age));
        memcpy(g_buffer, age, sizeof(age));
}


void fullname()
{
        read(0, &g_buffer[8], 32);
        fprintf(stdout, &g_buffer[8]);
        fflush(stdout);
}

void bio()
{
        char buffer[64];
        gets(buffer);
}

int main()
{
        alarm(60);
        system("echo \"hello world\"");
        fprintf(stdout, "what is your age? ");
        fflush(stdout);
        age();
        fprintf(stdout,"what is your full name? ");
        fflush(stdout);
        fullname();
        fprintf(stdout,"tell me something more about you: ");
        fflush(stdout);
        bio();
}

