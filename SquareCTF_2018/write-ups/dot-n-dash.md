# dot-n-dash

## Description

In this task we got:

* `dot-n-dash.html` which is both interface and engine for offline (does not have to be run in dedicated environment) string encoding and decoding without any key.
* `instructions.txt` file containing encoded data.

The whole `instructions.txt` file looks as follows:

> -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------.----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------.------------------------------  (...) about 370.000 more dots and dashes.

The most important parts of given code are methods responsible for string encoding and decoding:

```js
function _encode(input) {
    var a=[];
    for (var i=0; i<input.length; i++) {
        var t = input.charCodeAt(i);
        for (var j=0; j<8; j++) {
            if ((t >> j) & 1) {
                a.push(1 + j + (input.length - 1 - i) * 8);
            }
        }
    }

    var b = [];
    while (a.length) {
        var t = (Math.random() * a.length)|0;
        b.push(a[t]);
        a = a.slice(0, t).concat(a.slice(t+1));
    }

    var r = '';
    while (b.length) {
        var t = b.pop();
        r = r + "-".repeat(t) + ".";
    }
    return r;
}
// Everything below this line was lost due to cosmis radiation. The engineer who knows
// where the backups are stored already left.
function _decode(input) {
    return "";
}
```

So as We can see, our job is to write the body of `_decode()` method, and to do so We've to understand how encoding is done. Lets start analyzing the `_encode()` method by looking at the first loop:

```js
var a=[];
for (var i=0; i<input.length; i++) {
    var t = input.charCodeAt(i);
    for (var j=0; j<8; j++) {
        if ((t >> j) & 1) {
            a.push(1 + j + (input.length - 1 - i) * 8);
        }
    }
}
```

As We can see, the outer loop iterates through every char (`t`) in input string (`i` holds its index), the second loop iterates through every bit in given char (`j` holds its position). The `if` statement is executed only if `j` bit is set in char `t`. In the `if` statement the list `a` is extended with single number. Lets look at the expression that defines the number value from right to left:

* `(input.length - 1 - i) * 8` We can also write as `(input.length - 1 - i) << 3` so we can clearly see that three least significant bits of the resulting number will be unset. `input.length` is constant for each char in given input string, so that value of this subexpression will have smaller value for char at index `i` than for char at index `i - 1`.
* `j` is added to expression mentioned above, its value is from range $\langle0; 2^3)$ so it will be written at three least significant bits.
*  At the end, the value is incremented by one.

So every number added to list `a`, after decrementing its value by one, holds the information about:

* set bit position in given char (at three least significant bits) - `bit_pos = (a[x] - 1) & 0x7`
* relative char position in input string (at the rest of bits) - `char_pos = (a[x] - 1) >> 3`. `char_pos` for the first char will have the smallest value and `char_pos` for last char will have the biggest value.

Summing up, this loop is responsible for adding a single number to list `a` for each set bit in every char in input string. Moreover, We can recover the relative position of char that this set bit belongs to and position of this set bit in char.

Next loop in `_encode()` method is only responsible for shuffling the list `a`:

```js
var b = [];
while (a.length) {
	var t = (Math.random() * a.length)|0;
    b.push(a[t]);
    a = a.slice(0, t).concat(a.slice(t+1));
}
```

After this loop finishes its work, `b` list is just shuffled form of `a` list. Lets look at the last code block in `_encode()` method:

```js
var r = '';
while (b.length) {
    var t = b.pop();
    r = r + "-".repeat(t) + ".";
}
return r;
```

This loop creates the final encoded string. For each number in `b` it adds number of dashes equal to value of currently processed number and single dot afterwards.

## Solution

We can easily recover the `b` list just by counting the dashes till the firs occurrence of dot in encoded string and repeat this process until the end of encoded string read from `instructions.txt`.

We're unable to recover the `a` array without exploiting the `Math.random()`. But We don't have to, because each number in `b` holds all required information and recovering the initial number position in `a` is not necessary.

For each number in `b`, which represents single set bit in particular char, let's define:

```python
char_pos = (n - 1) >> 3
bit_pos = (n - 1) & 0x7
```

Then, We have to aggregate all numbers with the same `char_pos` and create corresponding char with value `0x00`. For each aggregated number, bit at `bit_pos` related to this number should be set in created char. 

Once all chars are constructed, We've to simply print them form the biggest value of corresponding `char_pos` to the smallest one:

>Instructions to disable C1: 
>1. Open the control panel in building INM035. 
>2. Hit the off switch. 
>
>Congrats, you solved C1! The flag is flag-bd38908e375c643d03c6.

`dot-n-dash.py` - Python script that automates the above steps.