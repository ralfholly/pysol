README
======

Summary
-------

PySol is a command-line utility that computes the rise/set and twilight times for a given date and location. 

Dependencies
------------

Please install [PyEphem](http://rhodesmill.org/pyephem/) first, i. e.
```
pip install pyephem
```

Examples
--------

```
# Determine coordinates of London
$ ./pysol.py query London
London, London, Greater London, England, United Kingdom
Latitude:  51.5073509
Longitude: -0.1277583

# Calculate sun rise/set for today.
$ ./pysol.py calc --lat 51.5074 --lon -0.12778
Sun rise:           2017-04-01 07:35:19    Sun set:          2017-04-01 20:34:22
Civil begin:        2017-04-01 07:00:48    Civil end:        2017-04-01 21:09:01
Nautical begin:     2017-04-01 06:20:57    Nautical end:     2017-04-01 21:49:06
Astronomical begin: 2017-04-01 05:37:14    Astronomical end: 2017-04-01 22:33:09

# Create a file when the sun goes down.
$ echo "touch /tmp/sunset" | at $(./pysol.py calc --lat 51.5074 --lon -0.12778 --set --at-format)
```

