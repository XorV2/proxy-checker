# proxy-checker
proxy checker is an open-source module used to check all types of proxies.

This is the code to check just 1 proxy

```python
from check import CheckSingle

IP = "proxyip"
PORT = int("proxyport")

works = CheckSingle("proxyip", int("proxyport"))

if works.check_http():
    print(f"{IP}:{PORT} is a working HTTP proxy")

if works.check_socks5():
    print(f"{IP}:{PORT} is a working SOCKS5 proxy")

if works.check_socks4():
    print(f"{IP}:{PORT} is a working SOCKS4 proxy")
```

if the proxy does not throw an exception whilst trying to perform something it is meant to do, CheckSingle will return True, if it throws an exception it will return False


# How do i check a file?
```python
from check import CheckFile

proxies : list[str] = CheckFile("http_proxies.txt").check_http()

for proxy in proxies:
    print(f"{proxy} is a working http proxy")
```

CheckFile().check_x() will return a list of all of the proxies in the file that responded without throwing an exception.

# How do i set a timeout
```python
works = CheckSingle("proxyip", int("proxyport"), timeout=int("proxytimeout"))

if works.check_http():
    print(f"proxy responded in under x seconds")

```
timeout should be an **absolute value** if it isn't the program will throw an error because the module will not fix your horrid code logic.