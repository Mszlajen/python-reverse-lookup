# Reverse Lookup

Implementation of a reverse lookup similar to [Beta](https://beta.cs.au.dk/) where parent classes have priority and decide when to allow the subclasses (or the instance) to extend its behaviour.

## Installation

Reverse Lookup is made using pure python metaprogamming interfaces so it can be installed easily from pypi

```bash
python -m pip install reverse_lookup
```

## Usage

Using Reverse Lookup is as simple as inhereting a class.

```python
from reverse_lookup import ReverseLookup

class A(ReverseLookup):
    ...
```

Now all instances of `A` will have a lookup that looks like `object -> A -> <A object>`.  
This works for subclasses too.

```python
class A(ReverseLookup):
    def m(self):
        return 'A'

class B(A):
    def m(self):
        return 'B'

B().m() # => 'A'
```

To allow subclasses to extend the logic you can use `Inner`.

```python
from reverse_lookup import ReverseLookup, Inner

class A(ReverseLookup):
    def m(self):
        return 'A' + Inner(self, A).m()
        
class B(A):
    def m(self):
        return 'B'

B().m() #=> 'AB'
```

Like the built-in `super`, `Inner` can be send any message and it will do a lookup for it starting at next step in the mro, it will fail with `AttributeError` if there is not a next implementation and special methods will need to be called explicitly.

The new lookup is compatible with descriptors and overriding some of the hooks in method such as `__str__`.

## Motivation

We mentioned that this could be posible using metaprogramming and I though it was a fun project.
