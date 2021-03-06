## radare2
`axt` - find references

`/ Pattern` - find "Pattern" in binary

`iI` - binary information

`iz` - strings ?

`is` - symbols

`ie` - entrypoints

`iM` - main

`oo` - reopen with read

`oo+` - reopen with read/write

`afvn [n_name] [o_name]` - rename variable

## gdb dump memory range to file:
`dump binary memory dump.bin addr_start addr_end`

## gdb scripting
```
$ cat script.gdb
gef config context.enable 0
pie break *0x6991
pie run < input

set $i = 0
while($i < 0x22)
    printf "%c", $edi
    set $i = $i+1
    c
end
$ gdb file -x script.gdb
```
## compilation stages
```
gcc -E -P compilation_example.c > compilation_example.i
gcc -S -masm=intel compilation_example.c
gcc -c compilation_example.c
gcc compilation_example.c
cp a.out a.out.stripped
strip --strip-all a.out.stripped

******* CREATED FILES *******
compilation_example.i: preprocessed source
compilation_example.s: assembly code
compilation_example.o: object file
a.out                : binary executable
a.out.stripped       : stripped binary executable
******* CREATED FILES *******

```

# command on port via ncat 
```
ncat -lkvp 1337 -e "/usr/bin/python3.6 `pwd`/echosvr.py"
```
# bash
## bash without aslr
`setarch $(arch) -R bash`
## redirections
`>` redirects *stdout* to a file

`2&>` redirects file handle "2" (almost always *stderr*) to some other file handle (it's generally written as `2>&1`, which redirects stderr to the same place as stdout).

`&>` and `>&` redirect both *stdout* and *stderr* to a file. It's normally written as `&>file` (or `>&file`). It's functionally the same as `>file 2>&1`.

`2>` redirects output to file handle 2 (usually *stderr*) to a file.
## cat without cat
`read xxx < /etc/passwd; echo $xxx` single line

`while read -r line; do echo $line; done < /etc/passwd` whole file

# binary
## patch binary at offset
`echo -e '\xC3' | dd of=myFile bs=1 seek=$((0x440)) count=1 conv=notrunc`

## create virtualenv with access to global packages
`mkvirtualenv --system-site-packages --python=$(which python) angr_p2`

## nmap
`sudo nmap -sS -p 1-500 -O 192.168.1.0/24` - stealth scan, ports range, identify OSes, address mask.
 
## bash misc
`( sleep 3;cat - )` -> runs new process for commands inside `()`. This process will sleep for 3 sec and then read from stdin.

`$(seq 1 2 10)` -> 1 3 5 7 9

`mkfifo <path>` -> create named FIFO pipe.

## git
`git config --global url.ssh://git@github.com/.insteadOf https://github.com/` - force ssh instead of https

remember ssh key password
```
eval `ssh-agent -s`
ssh-add
```
## tshark dump data
`tshark -r error_reporting.pcap -Y "icmp.type==0" -e "data.data" -Tfields`

## python
### draw lines/dots on image
```
from PIL import Image, ImageDraw
#                       x    y
img = Image.new('RGB', (30, 200), (255, 255, 255))
d = ImageDraw.Draw(img)
#     x    y
m = [(10, 100), (20, 100), (15, 150), (10, 100)]
d.line(m, fill=(0,0,0), width=2)
d.point(m, fill=(255,0,0))
img.save("image.png", "PNG")
```
