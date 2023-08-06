# htutil

HaoTian's Python Util

![version](https://img.shields.io/pypi/v/htutil)
![downloads](https://img.shields.io/pypi/dm/htutil)
![format](https://img.shields.io/pypi/format/htutil)
![implementation](https://img.shields.io/pypi/implementation/htutil)
![pyversions](https://img.shields.io/pypi/pyversions/htutil)
![license](https://img.shields.io/pypi/l/htutil)

## Install

```sh
pip install htutil
```

## Usage

### file

```python
from htutil import file
```

Refer to C# System.IO.File API, very simple to use.

```python
    s = 'hello'
    write_all_text('1.txt', s)
    # hello in 1.txt
    append_all_text('1.txt', 'world')
    # helloworld in 1.txt
    s = read_all_text('1.txt')
    print(s)  # helloworld

    s = ['hello', 'world']
    write_all_lines('1.txt', s)
    # hello\nworld in 1.txt
    append_all_lines('1.txt',['\npython'])
    # hello\nworld\npython in 1.txt
    s = read_all_lines('1.txt')
    print(s)  # ['hello', 'world', 'python']
```

### Log

```python
from htutil import log
from htutil.log import p
```

A powerful logger, support var name output.

```python
a = 3
p(a)
p(a-1)

b = bob()
p(b.a)
```

The output is

```txt
a = 3;2020-12-19 16:43:49;/Users/t117503445/Project/htutil/htutil/log.py:55
a-1 = 2;2020-12-19 16:43:49;/Users/t117503445/Project/htutil/htutil/log.py:56
b.a = 3;2020-12-19 16:43:49;/Users/t117503445/Project/htutil/htutil/log.py:58
```

You could change the output format.

```python
config(format = '${var_name} = ${value} ### ${time} ### ${file_name}:${line_number}')
p(a)
```

then the output is

```txt
a = 3 ### 2020-12-19 16:46:56 ### /Users/t117503445/Project/htutil/htutil/log.py:60
```

The default format is ${var_name} = ${value};${time};${file_name}:${line_number}

If you want to save the log output to file, you could use callback.

```python
def callback_example(string: str):
    file.append_all_text('1.log',string)

register_p_callback(callback_example)
a = 3
p(a)
```

lambda is also a good choice.

```python
register_p_callback(lambda string:file.append_all_text('1.log',string))
a = 3
p(a)
```

### cache

cache def result by pickle file.

```python
from htutil import cache
@cache.file_cache
def get_1():
    time.sleep(3)
    return 1
```

### counter

a simple counter based on dict.

```python
    c = Counter()
    c.add('1')
    c.add('1')
    c.add('2')

    print(c.to_dict()) # {'1': 2, '2': 1}

    c.dump() # same as print(c.to_dict())
```
