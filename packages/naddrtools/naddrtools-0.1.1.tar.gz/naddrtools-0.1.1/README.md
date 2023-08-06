# naddrtools
**naddrtools** is a simple library for manipulating IP addresses, ranges, and networks and acts as an extension of the netaddr module.

```
>>> import naddrtools as nat
>>> mylist = ["100.25.13.11", "172.20.31.0/24", "172.20.30.1 - 172.20.30.254"]
>>> ipset = nat.build_ipset(mylist, buff_network_ranges=True)
>>> print(ipset)
IPSet(['100.25.13.11/32', '172.20.30.0/23'])
>>> print(nat.convert_ipset_to_ranges_as_string(ipset))
100.25.13.11, 172.20.30.0 - 172.20.31.255
```

## Installing naddrtools
naddrtools is available on PyPI:

```console
$ python -m pip install naddrtools
```
