from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM


def get_out_ip():
    """
    获取本机 IP
    """
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


if __name__ == '__main__':
    print(get_out_ip())
    print(type(get_out_ip()))
