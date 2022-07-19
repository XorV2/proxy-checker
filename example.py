from check import CheckFile

# regular check for a file
proxies = CheckFile("http_proxies.txt").check_http()

for proxy in proxies:
    print(f"{proxy} works!")


# a timeout of 5 seconds for a file
proxies = CheckFile("http_proxies.txt", timeout=5).check_http()

for proxy in proxies:
    print(f"{proxy} responds in under 5 seconds!")


# a maximum number of threads
proxies = CheckFile("http_proxies.txt", max_threads=100).check_http()

for proxy in proxies:
    print(f"{proxy} works!")