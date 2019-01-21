## gdb

Dump memory range to file:

`dump binary memory dump.bin addr_start addr_end`

## command on port via ncat 

```
ncat -lkvp 1337 -e "/usr/bin/python3.6 `pwd`/echosvr.py"
```

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
