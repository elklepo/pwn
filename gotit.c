#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <string.h>

#define INPUT_SIZE 128

struct M {
    unsigned long long i;
    char title[12];
    char *content;
};

void printFlag() {
    system("/bin/cat flag.txt");
}

int main() {
    struct M *m;
    char buf[INPUT_SIZE] = {0};

    alarm(60);

    setvbuf(stdin, 0, _IOLBF, 0);
    setvbuf(stdout, 0, _IOLBF, 0);
    setvbuf(stderr, 0, _IOLBF, 0);

    m = (struct M *)malloc(sizeof(struct M));
    m->content = (char *)malloc(sizeof(char) * 1024);

    puts("Provide title: ");
    read(0, buf, INPUT_SIZE);
    strcpy(m->title, buf);

    puts("Provide content: ");
    read(0, buf, INPUT_SIZE);
    strcpy(m->content, buf);

    printf("title: %scontent: %s", m->title, m->content);

    return 0;
}

