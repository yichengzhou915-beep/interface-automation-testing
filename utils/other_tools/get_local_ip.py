#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        l_host = s.getsockname()[0]
    finally:
        s.close()

    return l_host


if __name__ == '__main__':
    print(get_host_ip())