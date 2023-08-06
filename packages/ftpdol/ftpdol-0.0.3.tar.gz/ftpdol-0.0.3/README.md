
# ftpdol
ftp with a simple (dict-like or list-like) interface


To install:	```pip install ftpdol```


A basic ftp persister.
Keys must be names of files.

```python
>>> from py2store.persisters.ftp_persister import FtpPersister
>>> s = FtpPersister()
>>> k = 'foo'
>>> v = 'bar'
>>> for _key in s:
...     del s[_key]
>>> len(s)
0
>>> s[k] = v
>>> s[k]
'bar'
>>> s.get(k)
'bar'
>>> len(s)
1
>>> list(s.values())
['bar']
>>> k in s
True
>>> del s[k]
>>> k in s
False
>>> len(s)
0
```
