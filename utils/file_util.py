import json
import socket


def loads_json(path):
    ds = []
    with open(path, encoding='utf') as f:
        for line in f.readlines():
            d = json.loads(line)
            ds.append(d)
    return ds


def load_txt(path):
    res = []
    with open(path, encoding='utf') as f:
        for line in f.readlines():
            line = line.strip()
            res.append(line)
    return res


def get_host_ip():
    """
    获取本机IP地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

