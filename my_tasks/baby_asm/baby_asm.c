#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <seccomp.h>
#include <sys/prctl.h>
#include <fcntl.h>
#include <unistd.h>

void sandbox()
{
    alarm(5);
    
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL)
    {
        printf("Contact admins.\n");
        exit(0);
    }

    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

    if (seccomp_load(ctx) < 0)
    {
        seccomp_release(ctx);
        printf("Contact admins.\n");
        exit(0);
    }
    seccomp_release(ctx);
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IOLBF, 0);
    
    char* shellcode = (char*)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);
    memset(shellcode, 0x90, 0x1000);

    puts("Holy Grail - './yo_bro_here_is_your_flag.txt'");
    printf("Give me your x64 shellcode: ");
    read(0, shellcode, 1000);

    sandbox();

    __asm__("xor %rax, %rax;"
            "xor %rbx, %rbx;"
            "xor %rcx, %rcx;"
            "xor %rdx, %rdx;"
            "xor %rsi, %rsi;"
            "xor %rdi, %rdi;"
            "xor %r8,  %r8;"
            "xor %r9,  %r9;"
            "xor %r10, %r10;"
            "xor %r11, %r11;"
            "xor %r12, %r12;"
            "xor %r13, %r13;"
            "xor %r14, %r14;"
            "xor %r15, %r15;");
    
    ((void (*)(void))shellcode)();
    
    return 0;
}