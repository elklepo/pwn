# minefield

## description

> We have a minefield in front of us. 
>
> We can either disarm those mines or jump over them.
>
> Let's go!

## exploitation

So basically I really fucked up because I accidentally removed the source code after implementation.

Good thing is that the easiest way to exploit this task requires only knowledge about `main()` function. Here is recovered `main()`:

```c
char* b[463];

int main()
{
  puts("Hello my friend. We need to pass this minefied to capture the flag. Are You ready?");
  sleep(2);

  puts("Do not step on this! Cut the wire, fast!");
  if (access("./bro/i/thougth/you/took/that/pliers/fff/.../So/we/are/gonna/die/here./only/\xde\xad\xbe\xef/will/be/left", F_OK) == -1)
  {
      return -1;
  }
  sleep(2);
  
  puts("There is a huge mine nearby! Don't even look there!");
  if (ptrace(PTRACE_TRACEME, 0, NULL, 0) == -1)
  {
      return -1;
  }
  sleep(2);
  foo0();
  
  puts("Watch out! There's another one!");
  if (fork() != 0)
  {
    abort();
  }
  sleep(2);
  foo1();
  
  alarm(1);
  puts("Move faster! This one will explode soon!");
  sleep(2);
  foo2();
  
  puts("Don't touch it!");
  *(char**)NULL = "pwned";
  sleep(2);
  foo3();
  
  puts("We did it! Thats our flag, I hope You took the smartphone?");
  sleep(2);
  
  puts(b);
  return 0;
}
```

Functions `foo0()`, `foo1()`, `foo2()` and `foo3()` are big, obfuscated methods that (when called in numerical order) reconstruct the ASCII data in `b[463]`.

`main()` is full of *mines*, code fragments that will cause early process termination.

There are a lot of possibilities to get rid of those mines. IMO the two easies ones:

 1. Run GDB and just jump over the nasty fragments
 2. Patch the binary and replace with NOPs all problematic instructions.

I chose the second option in my exploit.

If We defeat all the mines, the *message* will appear on stdout:

```
bbbbbbbwbbbbwwbbbbbbb
bwwwwwbwwwwbwwbwwwwwb
bwbbbwbwbbbwwwbwbbbwb
bwbbbwbwbwbwbwbwbbbwb
bwbbbwbwbbbwbwbwbbbwb
bwwwwwbwwbbwwwbwwwwwb
bbbbbbbwbwbwbwbbbbbbb
wwwwwwwwwwwbbwwwwwwww
bbbbwwbwbwbwbbwwbbbwb
bwwbbbwwwbbwwwbwbwbbw
bwbbwwbwwwbwwbwbwwbbb
bwbwbwwbwbbbbbwbwbwbw
bbwbwwbwwwwbwbbwbwbww
wwwwwwwwbwwwwbbbwwwbb
bbbbbbbwwbwbwbbbbwwww
bwwwwwbwwwbwbbwbbbbbw
bwbbbwbwwbbwwwwbwbwwb
bwbbbwbwbbwwbwbwbwwww
bwbbbwbwbwwbbbbwwbwww
bwwwwwbwbwwbwwbwwwwwb
bbbbbbbwbwwwwwbbbbwww
```

Now if We replace `'w'` with e.g. `' '` and `'b'` with `'#'` it is clear that We received a strange representation of QR code:

```
####### ####  #######
#     #    #  #     #
# ### # ###   # ### #
# ### # # # # # ### #
# ### # ### # # ### #
#     #  ##   #     #
####### # # # #######
           ##        
####  # # # ##  ### #
#  ###   ##   # # ## 
# ##  #   #  # #  ###
# # #  # ##### # # # 
## #  #    # ## # #  
        #    ###   ##
#######  # # ####    
#     #   # ## ##### 
# ### #  ##    # #  #
# ### # ##  # # #    
# ### # #  ####  #   
#     # #  #  #     #
####### #     ####   
```

Last thing to do is to generate the valid QR code image and decode it.

![qr_img](./qr_img.png)

[exploit.py](./exploit.py) automates steps described above.
