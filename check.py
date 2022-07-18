#!/usr/bin/python3
# encoding='utf-8'

from concurrent.futures import ThreadPoolExecutor

from socks import (
    HTTP,
    SOCKS4,
    SOCKS4_ERRORS,
    SOCKS5,
    GeneralProxyError,
    HTTPError,
    ProxyConnectionError,
    ProxyError,
    SOCKS4Error,
    SOCKS5Error,
    socksocket,
)

TEST_HOST = "www.google.com"


class CheckSingle:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"

    def __init__(self, host, port, timeout=1):
        self.host = host
        self.port = port
        self.timeout = timeout

    def check_http(self):
        """
        Checks a HTTP proxy and checks if the proxy responds to the source
        port specified and checks if the data can be send to a HTTP server
        without an error being thrown.
        """

        with socksocket() as sock:
            try:
                sock.setproxy(HTTP, self.host, self.port)
                sock.settimeout(self.timeout)
                sock.connect((TEST_HOST, 80))
                sock.sendall(
                    f"GET / HTTP/1.1\r\nHost: google.com\r\nUser-Agent: {self.user_agent}\r\nConnection: keep-alive\r\n\r\n".encode()
                )

            except (ProxyConnectionError, GeneralProxyError, HTTPError, ProxyError):
                return False

            else:
                return True

    def check_socks4(self):
        """
        Checks a socks4 proxy to see if it responds to the specified source
        ip address and port. If it does try to connect to a TCP port and
        write to the socket and then close it, if it does that without
        throwing an error then return True otherwise return False
        """

        with socksocket() as sock:
            try:
                sock.settimeout(self.timeout)
                sock.setproxy(SOCKS4, self.host, self.port)
                sock.connect(("1.1.1.1", 80))
                sock.send(b"Hello, world!")

            except (GeneralProxyError, ProxyConnectionError, ProxyError, SOCKS4Error):
                return False

            else:
                return True

    def check_socks5(self):
        """
        Checks a socks5 proxy to see if it responds to the specified source
        ip address and port. If it does try to connect to a TCP port and
        write to the socket and then close it, if it does that without
        throwing an error then return True otherwise return False
        """

        with socksocket() as sock:
            try:
                sock.settimeout(self.timeout)
                sock.setproxy(SOCKS5, self.host, self.port)
                sock.connect(("1.1.1.1", 80))
                sock.send(b"Hello, world!")

            except (GeneralProxyError, ProxyConnectionError, ProxyError, SOCKS5Error):
                return False

            else:
                return True


class CheckFile:
    def __init__(self, filename, path="", timeout=1, max_threads=1000):
        with open(f"{path}{filename}", "r") as f:
            self.contents = [line.strip("\n") for line in f.readlines()]

        self.max_threads = max_threads
        self.working = []
        self.timeout = timeout

    @staticmethod
    def _format_proxies(proxies: list[str]) -> dict[str, int]:
        """
        takes a list of proxies and returns a dictionary of:
          {ip:port}
        """

        formatted_proxies = dict()
        for proxy in proxies:
            part_proxy = proxy.partition(":")
            # part_proxy[0] is the ip address of the proxy
            # part_proxy[1] is the partition character, ':'
            # part_proxy[2] is the port number of the proxy server
            formatted_proxies[part_proxy[0]] = int(part_proxy[2])

        return formatted_proxies

    def _check(self, ip, port, type):
        """
        This function is literally just so i can thread it to make
        the checking of alot of proxies easier

        if the proxy works correctly then we append it to the list
        of working proxies.
        """

        type = type.lower()

        if type == "http":
            if CheckSingle(ip, port, timeout=self.timeout).check_http():
                self.working.append(f"{ip}:{port}")

        elif type == "socks5":
            if CheckSingle(ip, port, timeout=self.timeout).check_socks5():
                self.working.append(f"{ip}:{port}")

        elif type == "socks4":
            if CheckSingle(ip, port, timeout=self.timeout).check_socks4():
                self.working.append(f"{ip}:{port}")

    def check_http(self):
        """
        write this documentation
        """

        self.content = self._format_proxies(self.contents)

        with ThreadPoolExecutor(self.max_threads) as executor:
            for (ip, port) in self.content.items():
                executor.submit(self._check, ip=ip, port=port, type="http")

        return self.working

    def check_socks5(self):
        """
        write this documentation
        """

        self.content = self._format_proxies(self.contents)

        with ThreadPoolExecutor(self.max_threads) as executor:
            for (ip, port) in self.content.items():
                executor.submit(self._check, ip=ip, port=port, type="socks5")

        return self.working

    def check_socks4(self):
        """
        write this documentation
        """

        self.content = self._format_proxies(self.contents)

        with ThreadPoolExecutor(self.max_threads) as executor:
            for (ip, port) in self.content.items():
                executor.submit(self._check, ip=ip, port=port, type="socks4")

        return self.working
