Cache function return value for given call arguments. 

```
gcc victim.c -O0 -o victim
make
$PIN_ROOT/pin -t obj-intel64/cache_function_calls.so -- ./victim ; cat cache_function_calls.log
```

