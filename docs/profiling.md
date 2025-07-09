# Profile import times and code

2025-05-19, @schluppeck

Scripts can take a bit of time to startup on first run (pre-compile?). They will then run faster on subsequent runs. This is especially true for large packages like `numpy` and `pandas`.

## To look at what takes long

We can use the `-X importtime` flag to see how long each module takes to import. This is useful to identify slow imports in our code.

```bash
## to get timings of imports, we can use built in logging
python -X importtime eccLoc.py 2> import_perf.log

## slightly more advanced, but also more useful, is to use cProfile
# this will give us a profile of the whole program
python -m cProfile -o my_program.prof eccLoc.py

# after pip install snakeviz
snakeviz my_program.prof
```
