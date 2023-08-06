# meowhash-python

> Safe bindings to extremely high performance hash function Meow Hash.

## About

Meow hash is an extremely fast non-cryptographic hash function. More details can
be found [here](https://mollyrocket.com/meowhash).

This library is a safe way of using Meow hash on any platform as an error will
be thrown if the target machine does not support the requisite SIMD processor
features.

## Installation

```bash
$ pip install meowhash-python
$ pip install git+https://github.com/Pebaz/meowhash-python
```

## Usage

```python
from meow_hash import MeowHash

hash_ = MeowHash(b'Hello World!')
hash_.digest()  # Bytes
hash_.hexdigest()  # Hex string
hash_.hash()  # 128 bit hash
```
