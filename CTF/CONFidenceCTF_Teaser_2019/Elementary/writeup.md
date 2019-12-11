# Elementary

`elementary` binary expects password of 104 characters. In function `checkFlag()` each password character is validated by calling different function for each character bit. Chars are validated in a *random* order, so as bits for particular byte. There are a total of 832 functions for bits validation, each of them returns true if bit is set correctly, false otherwise.  

```c
//main
printf("%s", checkFlag(pass) ? "Success!" : "Wrong!");

bool checkFlag(const char pass[104])
{
    if(!function0((pass[64] >> 4) & 0x01)
        mov eax, 0; ret;
    if(!function1((pass[64] >> 1) & 0x01)
        mov eax, 0; ret;
    if(!function2(pass[64] & 0x01)
        mov eax, 0; ret;
    if(!function3((pass[64] >> 7) & 0x01)
        mov eax, 0; ret;
    if(!function4((pass[64] >> 3) & 0x01)
        mov eax, 0; ret;
    if(!function5((pass[64] >> 6) & 0x01)
        mov eax, 0; ret;
    if(!function6((pass[64] >> 5) & 0x01)
        mov eax, 0; ret;
    if(!function7((pass[64] >> 2) & 0x01)
        mov eax, 0; ret;
    ...
    if(!function824((pass[4] >> 2) & 0x01)
        mov eax, 0; ret;
    if(!function825((pass[4] >> 7) & 0x01)
        mov eax, 0; ret;
    if(!function826((pass[4] >> 5) & 0x01)
        mov eax, 0; ret;
    if(!function827((pass[4] >> 1) & 0x01)
        mov eax, 0; ret;
    if(!function828(pass[4] & 0x01)
        mov eax, 0; ret;
    if(!function829((pass[4] >> 6) & 0x01)
        mov eax, 0; ret;
    if(!function830((pass[4] >> 3) & 0x01)
        mov eax, 0; ret;
    if(!function831((pass[4] >> 4) & 0x01)
        mov eax, 0; ret;
    //success
    mov eax, 1; ret;
}
```

First, lets apply following patches to binary:

1. `main()` passes `checkFlag()` return value as process exit code.
2. If `checkFlag()` fails on call to `functionX()`  it returns `x % 128` instead of `0` every time. Thanks to this, We're able to estimate how far our input was validated.  `% 128` just to make sure that there will be no problems with process exit code fitting in `uint8_t`.
3. `checkFlag()` returns `128` when password passed validation.

That is how it looks after patching:

```c
//main
call checkFlag
leave
ret

bool checkFlag(const char pass[104])
{
    if(!function0((pass[64] >> 4) & 0x01)
        mov eax, 0; ret;
    if(!function1((pass[64] >> 1) & 0x01)
        mov eax, 1; ret;
    if(!function2(pass[64] & 0x01)
        mov eax, 2; ret;
    if(!function3((pass[64] >> 7) & 0x01)
        mov eax, 3; ret;
    if(!function4((pass[64] >> 3) & 0x01)
        mov eax, 4; ret;
    if(!function5((pass[64] >> 6) & 0x01)
        mov eax, 5; ret;
    if(!function6((pass[64] >> 5) & 0x01)
        mov eax, 6; ret;
    if(!function7((pass[64] >> 2) & 0x01)
        mov eax, 7; ret;
    ...
    if(!function824((pass[4] >> 2) & 0x01)
        mov eax, 56; ret;
    if(!function825((pass[4] >> 7) & 0x01)
        mov eax, 57; ret;
    if(!function826((pass[4] >> 5) & 0x01)
        mov eax, 58; ret;
    if(!function827((pass[4] >> 1) & 0x01)
        mov eax, 59; ret;
    if(!function828(pass[4] & 0x01)
        mov eax, 60; ret;
    if(!function829((pass[4] >> 6) & 0x01)
        mov eax, 61; ret;
    if(!function830((pass[4] >> 3) & 0x01)
        mov eax, 62; ret;
    if(!function831((pass[4] >> 4) & 0x01)
        mov eax, 63; ret;
    //success
    mov eax, 128; ret;
}
```

Last thing We need is the order in which bytes are validated. `objdump -d` + few minutes with regex worked just fine.

Now We can initialize password to `'A' * 104` and brute force it, byte after byte, using process exit code as a feedback function.

[exploit.py](./exploit.py) - Python script exploit.

> p4{I_really_hope_you_automated_this_somehow_otherwise_it_might_be_a_bit_frustrating_to_do_this_manually}