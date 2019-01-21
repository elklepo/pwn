## gdb

Dump memory range to file:

`dump binary memory dump.bin addr_start addr_end`

## command on port via ncat 

```
ncat -lkvp 1337 -e "/usr/bin/python3.6 `pwd`/echosvr.py"
```
