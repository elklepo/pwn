# echoechoechoecho and why I failed.

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