# Truncatable primes

A Python library that generates that generates sequences of truncatable
prime numbers and derivatives of the sequences in the form of a package
that can be installed and imported.

A truncatable prime is still prime when number is truncated.  For example,
317 is a left truncatable prime because 17 and 7 are prime.  It is also a
right truncatable prime because 31 and 3 are prime.

The intention of this library is to provide code that is reasonably efficient
and readable.  It is not difficult to track down cryptic one-liner code
that produces identical results.

## Getting Started

Python 3 is assumed.

### Installing

Using the source code from github
```
git clone https://github.com/harry-zuzan/trprimes.git
cd trprimes
python setup.py install

```

Using pip
```
pip install trprimes

```


### Examples
```
from trprimes import trunc

# the number of left truncatable primes
trunc.count_ltrunc()

# the largest of left truncatable prime
trunc.largest_ltrunc()

# iterate through left truncatable primes in ascending order
ltp = trunc.ordered_ltrunc()
next(ltp)

```


