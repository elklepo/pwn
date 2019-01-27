# gdb
## Dump memory range to file:
`dump binary memory dump.bin addr_start addr_end`
## gdb scripting
```
$ cat scrip.gdb
gef config context.enable 0
pie break *0x6991
pie run < input

set $i = 0
while($i < 0x22)
    printf "%c", $edi
    set $i = $i+1
    c
end
$ gdb -x script.gdb
```

# command on port via ncat 
```
ncat -lkvp 1337 -e "/usr/bin/python3.6 `pwd`/echosvr.py"
```
# bash
## redirections
`>` redirects *stdout* to a file

`2&>` redirects file handle "2" (almost always *stderr*) to some other file handle (it's generally written as `2>&1`, which redirects stderr to the same place as stdout).

`&>` and `>&` redirect both *stdout* and *stderr* to a file. It's normally written as `&>file` (or `>&file`). It's functionally the same as `>file 2>&1`.

`2>` redirects output to file handle 2 (usually *stderr*) to a file.

# networking
## nmap
`sudo nmap -sS -p 1-500 -O 192.168.1.0/24` - stealth scan, ports range, identify OSes, address mask.
 
## misc
`( sleep 3;cat - )` -> runs new process for commands inside `()`. This process will sleep for 3 sec and then read from stdin.

`$(seq 1 2 10)` -> 1 3 5 7 9

`mkfifo <path>` -> create named FIFO pipe.
