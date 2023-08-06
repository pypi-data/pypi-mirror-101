python-radix library
====================

The library contains tools for representing natural numbers in a given base,
or to current any numeral representing a natural number between two bases.
Currently any base between 2 and 36 is supported.



Python-radix usage examples
---------------------------
Python-radix has both procedural and object-oriented solutions.

### Procedural way example

    # to convert numeral 4 from base 10 to base 2
    >>> cast('4', 10, 2)
    '100'

    # to convert the integer 4 to base 2
    >>> cast(4, None, 2)

Note that since the first argument is a number, rather than a numeral,
the second parameter is irrelevant, so None is used.

### Object oriented way example
    >>> # create an object to find the base 2 representation of any natural number
    >>> new = Converter(None, 2)
    >>> new.convert(4)
    '100'
    >>> # create an object to find the base 2 representation of any base 10 numeral
    >>> new = Converter(10, 2)

    >>> new.convert('4')
    '100'

**Using characters as digits**

    # the digits 0 through 9 are succeeded by the lower case ASCII alphabet
    >>> cast('a', 16, 10)
    '10'
