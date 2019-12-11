/*
 * gcc just_guess.c -o just_guess
 */

#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

#define NO_NUMBERS (8)
uint64_t target_numbers[NO_NUMBERS];
uint64_t guessed_numbers[NO_NUMBERS]; // = { 0xFF }; uncomment for hard-mode

bool guess()
{
    for(size_t i = 0; i < NO_NUMBERS; ++i)
    {
        printf("[%lu]> ", i + 1);
        fflush(stdout );
        scanf("%lu", &guessed_numbers[i]);
        while ( getchar()!='\n' );
        
        guessed_numbers[i] ^= target_numbers[i];
        if(guessed_numbers[i] != 0)
            return false;
    }
    return true;
}

int main()
{
    int fd = open("/dev/urandom", O_RDONLY);
    if(fd == -1)
        goto ERR_CLEANUP;
    if(read(fd, target_numbers, sizeof(target_numbers)) != sizeof(target_numbers))
        goto ERR_CLEANUP;

    printf("You are going to play a lottery, just guess %d 64-bit numbers and You'll get the flag!\n", NO_NUMBERS);
    fflush(stdout);

    while( !guess() )
    {
        puts("Damn, You missed it! One more time?");
        fflush(stdout);
    }
    
    puts("Congratz! Here is Your flag:");
    puts("flag{flagflagflagflagflagflag}");
    return 0;

ERR_CLEANUP:
    puts("Contact admins, something bad happened.");
    return -1;
}
