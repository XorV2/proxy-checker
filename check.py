"""
 * Copyright (C) 2022 XorV2
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

#!/usr/bin/python3
# encoding='utf-8'

from concurrent.futures import ThreadPoolExecutor
from http.request import _returned_correct_data

from socks import (
    HTTP,
    SOCKS4,
    SOCKS5,
    socksocket,
)


class CheckSingle:
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
                sock.set_proxy(HTTP, self.host, self.port)
                sock.settimeout(self.timeout)
                sock.connect(("www.google.com", 80))
                sock.sendall(
                    f"GET / HTTP/1.1\r\nHost: www.google.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36\r\nConnection: keep-alive\r\n\r\n".encode()
                )
                data = sock.recv(1024).decode().lower()
                if _returned_correct_data(data):
                    return True
                return False

            except:
                return False

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
                sock.set_proxy(SOCKS4, self.host, self.port)
                sock.connect(("1.1.1.1", 80))
                sock.send(b"Hello, world!")
                return True

            except:
                return False

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
                sock.set_proxy(SOCKS5, self.host, self.port)
                sock.connect(("1.1.1.1", 80))
                sock.send(b"Hello, world!")
                return True

            except:
                return False


class CheckFile:
    def __init__(self, filename, timeout=1, max_threads=1000):
        with open(filename, "r") as f:
            self.contents = f.readlines()

        self.max_threads = max_threads
        self.working = []
        self.timeout = timeout

    @staticmethod
    def _format_proxies(proxies):
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
            formatted_proxies[part_proxy[0]] = int(part_proxy[2].strip("\n"))

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

        else:
            if CheckSingle(ip, port, timeout=self.timeout).check_socks4():
                self.working.append(f"{ip}:{port}")

    def check_http(self):
        """
        for each proxy in the file check if the proxy works
        correctly. Read the CheckSingle.check_http docstring
        for more information.
        """

        self.content = self._format_proxies(self.contents)

        with ThreadPoolExecutor(self.max_threads) as executor:
            for (ip, port) in self.content.items():
                executor.submit(self._check, ip=ip, port=port, type="http")

        return self.working

    def check_socks5(self):
        """
        for each proxy in the file check if the proxy works
        correctly. Read the CheckSingle.check_socks5 docstring
        for more information.
        """

        self.content = self._format_proxies(self.contents)

        with ThreadPoolExecutor(self.max_threads) as executor:
            for (ip, port) in self.content.items():
                executor.submit(self._check, ip=ip, port=port, type="socks5")

        return self.working

    def check_socks4(self):
        """
        for each proxy in the file check if the proxy works
        correctly. Read the CheckSingle.check_socks4 docstring
        for more information.
        """

        self.content = self._format_proxies(self.contents)

        with ThreadPoolExecutor(self.max_threads) as executor:
            for (ip, port) in self.content.items():
                executor.submit(self._check, ip=ip, port=port, type="socks4")

        return self.working
