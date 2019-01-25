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
## $(seq x y z)
```
$ echo $(seq 1 2 50)
1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 41 43 45 47 49
```
