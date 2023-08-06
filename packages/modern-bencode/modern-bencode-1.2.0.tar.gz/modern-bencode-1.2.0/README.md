# Modern bencode

A simple library for decoding/encoding bencoded data.

There are other bencode related libraries out there, but most of them:
- are created a long time ago and don't have active maintainers anymore
- don't have any docs at all or have very limited docs
- don't have any tests at all or have only partial test coverage
- use C extensions to make them faster, which can:
  - create problems when compiling on different platforms
  - make debugging more complicated (if you get a "Segmentation fault" error)

So, here is one more bencode library. Pluses:
- it has an active maintainer
- it has docs (both here and for all code) and human readable error messages
- it has type annotations (so you can see what each function takes/returns)
- it has 100% test coverage (+uses black, isort, flake8, mypy, pylint)
- it is written in pure Python and has no dependencies 

Minuses:
- it requires Python >= 3.7
- it is slower than libraries, which use C extensions (still, decoding  
  a regular torrent file takes up to a few milliseconds on a regular VPS)

## Installation
```
pip install modern-bencode
```
The library requires Python >= 3.7

## Usage
```python
from bencode import decode, decode_torrent, encode, encode_torrent

assert decode(b"li123e3:abce") == [123, b"abc"]
assert encode([123, b"abc"]) == b"li123e3:abce"

with open("my-torrent-file.torrent", "rb") as source_file:
    data = source_file.read()
    print(decode(data))
    print(decode_torrent(data, encoding="utf8"))
    assert data == encode_torrent(decode_torrent(data, encoding="utf8"))
```

## Notes

**bencode.decode** converts bencoded data to a Python object. It gets *bytes*  
and:
- either returns a Python object (*bytes*, *dict*, *int* or *list*)
- or raises a ValueError when decoding is not possible. The error message will  
  contain a human readable explanation why exactly it is not possible, for 
  example:
```
Cannot decode an integer, reached the end of the bencoded 
string before the end marker was found. Most likely the 
bencoded string is incomplete or incorrect.
```

**bencode.encode** converts a Python object to bencoded data. It gets a Python  
object (*bytes*, *dict*, *int* or *list*) and:
- either returns a bencoded string (as *bytes*)
- or raises a ValueError when encoding is not possible. The error message will  
  contain a human readable explanation why exactly it is not possible, for 
  example:
```
Cannot encode data: objects of type <class 'set'> are not supported.
```

**bencode.decode_torrent** converts torrent data to a Python object. It gets  
torrent data (as *bytes*), an optional 
[encoding](https://docs.python.org/3.7/library/codecs.html#standard-encodings) 
and:
- either returns a Python *dict*, where all keys and most values are strings.  
  Values are decoded:
  - using utf8 (if the key ends with ".utf-8" suffix, like "name.utf-8")
  - using the provided encoding (for other human readable fields)
  - as hex (for binary fields)
- or raises UnicodeDecodeError/ValueError when decoding is not possible.

**bencode.encode_torrent** converts torrent (as *dict*) to bencoded data. Just  
a mirror function for the previous one, deals with encoding in the same way.  
Raises UnicodeEncodeError/ValueError when encoding is not possible.

## Bugs

Feel free to create an issue [here](https://github.com/retonato/modern-bencode/issues)
if you find a bug or some error message is not clear enough.