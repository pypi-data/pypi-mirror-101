# Necessity

> *"Ale is my bear necessity."* - Pandaren Brewmaster

# Usage

```python

>>> import pandas as pd
>>> from necessity import count_column, sample_by_percentile

>>> data = ['foo'] * 100 + ['bar'] * 20 + ['blah'] * 50
>>> data += ['abc'] * 30 + ['xyz'] * 20 + ['bear'] * 10
>>> df = pd.DataFrame({'things': data})

>>> count_column(df, 'things')
foo     100
blah     50
abc      30
bar      20
xyz      20
bear     10
Name: things, dtype: int64

>>> count_column(df, 'things', normalize=True)
foo     0.434783
blah    0.217391
abc     0.130435
xyz     0.086957
bar     0.086957
bear    0.043478
Name: things, dtype: float64

>>> sample_by_percentile(df, 'things',bins=[0.0, 0.25, 0.75, 1.0], sample_sizes=[2, 1, 1])
['bear', 'bar', 'abc', 'foo']
```

```python
>>> import pandas as pd
>>> from necessity import count_x_concat_y

>>> data = {'thing': ['foo', 'bar', 'foo', 'duh', 'meh', 'hello', 'meh', 'world'],
        'lol': [['apple', 'orange'], ['pear'], ['cherry', 'banana', 'apple', 'apple'], ['strawberry', 'banana'],
                ['apple', 'pear'], ['strawberry', 'apple', 'banana'], ['pear'],  ['apple']]
       }

>>> df = pd.DataFrame(data)
>>> df
   thing                             lol
0    foo                 [apple, orange]
1    bar                          [pear]
2    foo  [cherry, banana, apple, apple]
3    duh            [strawberry, banana]
4    meh                   [apple, pear]
5  hello     [strawberry, apple, banana]
6    meh                          [pear]
7  world                         [apple]

>>> count_x_concat_y(df, column_x='thing', column_y='lol')
                                                 lol  count
thing                                                      
bar                                           [pear]      1
duh                             [strawberry, banana]      1
foo    [apple, orange, cherry, banana, apple, apple]      2
hello                    [strawberry, apple, banana]      1
meh                              [apple, pear, pear]      2
world                                        [apple]      1
```


```python
>>> import pandas as pd
>>> from necessity import count_x_concat_y, sum_str

>>> data = {'thing': ['foo', 'bar', 'foo', 'duh', 'meh', 'hello', 'meh', 'world'],
        'lol': ['orange', 'green', 'red', 'red', 'pink', 'yellow', 'red', 'green'],
       }

>>> count_x_concat_y(df, column_x='thing', column_y='lol', concat_func=sum_str)
                                                  lol  count
thing                                                      
bar                                           [green]      1
duh                                             [red]      1
foo                                     [orange, red]      2
hello                                        [yellow]      1
meh                                       [pink, red]      2
world                                         [green]      1
```
