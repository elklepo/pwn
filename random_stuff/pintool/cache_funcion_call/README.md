Cache function return value for given call arguments using two methods:
 1) `cache_function_calls.cpp` - more complicated, but more 1337 way. 
 2) `cache_function_calls_probe.cpp` - less complicated, utilizes Pin Tool probing.

Both use `RTN_FindByName()` because symbols are present. If I strip the binary and change it to `RTN_FindByAddress()` Pin Tool is not able to find `foo()`, it returns address to `_start()`... Maybe I'm stupid or it is a Pin Tool limitation.

In case of stripped binary, 1) is easily portable by hooking first instruction of `foo()` to `foo_entry_hook()` and all `foo()` `ret`s to `foo_ret_hook()`. I'm not sure if it is possible to port 2) to work with stripped binary.


```
gcc victim.c -O0 -o victim

optional:
    mv cache_function_calls_probe.cpp cache_function_calls.cpp

make
$PIN_ROOT/pin -t obj-intel64/cache_function_calls.so -- ./victim
```

