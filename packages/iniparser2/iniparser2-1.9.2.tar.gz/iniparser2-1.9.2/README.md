# iniparser2

[![Build Status](https://travis-ci.com/HugeBrain16/iniparser2.svg?branch=main)](https://travis-ci.com/HugeBrain16/iniparser2)  

**iniparser2** is An INI parser or a Config parser.  

this package is the improved version of [**iniparser**](https://github.com/HugeBrain16/iniparser) with more features.

---

# Quick Start

## Installation

to install the package see the following step below
  
`pip install iniparser2` || `python -m pip install iniparser2`    
from source: `python setup.py install`  

## Examples  
`test.ini`:
```ini
name = Mike Hawk
```
  
`test.py`:  
```py
from iniparser2 import INI

x = INI('test.ini')
data = x.read()

print(data)
```
  
#### Output:
```py
{'name': 'Mike Hawk'}
```
  
using `with` keyword  
  
`test.ini`:
```ini
name = Mike Hawk
```
  
`test.py`:  
```py
from iniparser2 import INI

with INI('test.ini') as i:
    print(i.read())
```
#### Output:
```py
{'name': 'Mike Hawk'}
```

parse without file
```py
import iniparser2

x = """
name = Mike Hawk
"""
x = iniparser2.parse(x)
print(x)
```

INI binary format

```py
import iniparser2

ex_data = {
    "slots": 20,
    "name": "no"
}

x = iniparser2.INI_BIN('test.ini')
x.write(ex_data)
data = x.read()

print(data)
```