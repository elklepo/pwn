# one_time_pad

## description

> I've heard that one-time pad is impossible to break, so You'll never get this flag.
>
> Don't even try.
>
> nc endpoint 1337

## solution

`srand(time(NULL))` is of course the exploitable vulnerability. 

The goal is to recover the one-time pad key used to encrypt the flag. 

We can do this by finding the seed that was used to initialize the libc pseudorandom number generator. 

`time(NULL)`  returns the time as the number of **seconds** since the Epoch, 1970-01-01 00:00:00 +0000 (UTC), so it is possible to easily recover all seeds generated within single day.

## exploit

Once We get the encrypted flag from remote, We have to get current `curr_time = time(NULL)` value.

Final step is to brute all possible one-time pad keys generated with seed from range `<curr_time - delta ; curr_time + delta>`. 

Brute-force is necessary due to slight time differences on remote and local machine.

One last thing is that we have to use exact same libc version that binary uses to make sure that we use the same pseudorandom number generator. libc version can be easily determined by calling `ldd` on binary.

[exploit.py](./exploit.py) automates steps described above.
