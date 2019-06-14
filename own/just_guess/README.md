# just_guess

## description
> All You need to do is guess a few numbers.
>
> Easy Peasy
>
> nc endpoint 1337 

## solution
We need to observe three things:

1. Array with guessed numbers is not cleaned between attempts.
2. Guessed number is XORed with expected number.
3. `scanf()` does not update destination location when parsing failed (In our case - not number value was passed)

#### version 1

`uint64_t guessed_numbers[NO_NUMBERS];`

Due to the fact that `guessed_numbers` array is located in 0 initialized section the easiest exploit is to pass non-numeric value 256 times.

#### version 2 

`uint64_t guessed_numbers[NO_NUMBERS] = { 0xFF };`

Due to the fact that `guessed_numbers` array is now initialized to non-zero value, we have to use non-trivial approach.

The idea is to pass `0` for number `n`, then it is XORed with expected value and verification fails but we have expected number in memory (`0 ^ expected_val == expected_val`). 

In one of next attempts we need to pass non numeric value for number `n` and the verification will pass. 

Now we need to write fancy algorithm to pass 10 numbers

[exploit.py](exploit.py)
