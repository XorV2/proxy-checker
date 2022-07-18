# proxy-checker
proxy checker is an open-source module used to check all types of proxies.

To simply check one proxy run this command

```

```


# How do i check a file?
```python
proxies = CheckFile("http_proxies.txt", timeout=5).check_http()

for proxy in proxies:
    print(f"{proxy} responds in under 5 seconds!")
```