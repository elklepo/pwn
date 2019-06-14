# badxor

## description
> I've created very secure encryption algorithm which uses 128-bit keys.
>
> It's called "badxor".
>
> The implementation is only few lines in python!
```python
key = bytearray( *** key - 16 bytes array ***)
msg = *** message to encode - string ***

ciphertext = bytearray()
for i, c in enumerate(msg):
    ciphertext.append(ord(c) ^ key[i % len(key)])

with open("secret_msg.dat", 'wb') as secret_msg:
    secret_msg.write(ciphertext)
```
> You'll never break it!

## solutions
### manual solution 
 1. Split ciphertext to 16 subciphertexts (every 16 byte, starting from byte 0, 1, 2 ... 15)
 2. Find most common byte in each subciphertext and XOR it with `0x20(' ')` because `0x20(' ')` is usually most common char. The resulting byte is Your n-th key byte.
 3. XOR ciphertext with retreived key.

[exploit.py](exploit.py) - automated steps mentioned above

### xortool solution
```
$ xortool ./secret_msg.dat
The most probable key lengths:
   2:   9.3%
   4:   10.7%
   6:   7.9%
   8:   15.1%
  10:   6.6%
  12:   7.6%
  16:   19.2%
  24:   7.4%
  32:   10.1%
  48:   6.2%
Key-length can be 4*n
Most possible char is needed to guess the key!

$ xortool ./secret_msg.dat -l 16 -c ' '
1 possible key(s) of length 16:
8\xa5\xd0\x89r\xf1\x8a\x90\xb1\xcfBg\x10q\x10\xb2
Found 1 plaintexts with 95.0%+ valid characters
See files filename-key.csv, filename-char_used-perc_valid.csv

$ cat ./xortool_out/0.out
...
Ok, that's enough. Here's Your flag: flag{flagflagflagflagflag} 
```
