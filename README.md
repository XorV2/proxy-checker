# proxy-checker


# How do i check a file?
```
proxies = CheckFile("http_proxies.txt", timeout=5).check_http()

for proxy in proxies:
    print(f"{proxy} responds in under 5 seconds!")
```