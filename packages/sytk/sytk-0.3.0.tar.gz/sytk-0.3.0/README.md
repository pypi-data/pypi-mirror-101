# ___sytk___
Some tools making life a little easier :)

## EzParser
A simple html parser supporting recursive searching.
## Logger
Pre-defined `logging.Logger`.

## @print2file
+ Redirect all the context printed by `print()` into file named `{file}-{func}.txt`.
+ It can also catch Exception.
## @timer
Just as the name implies.The return value of the decorated function will turn to `(return_value, duration)`.

## debug
### @debug
+ Show `parameters` and `return value` of the decorated function in a vivid color.
+ Meanwhile, in the same usage with `print()`, `d_print()`is also available to show the debug information in functions decorated with `@debug`.
### d_print()
same usage with `print()`.
### clean()
Delete code lines containing '@debug' and 'd_print'. It is used to turn projects into productions.

## hack
### get_admin()
Get admin right for the script.
