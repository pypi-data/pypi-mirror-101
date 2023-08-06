## pycomma
A python library designed to allow csv data processing workflows completely within a python shell 

[Documentation](https://jordankobewade.github.io/pycomma)


### Quickstart

``` pip install pycomma ```
``` 
from pycomma.comma import Comma 
comma = Comma("data.csv")
comma.prepare()
comma.show()
```