import json

class JSONProxy:
    @classmethod
    def convert_proxy_to_dict(cls, proxy_string: str) -> dict:
        scheme = None
        hostname = None
        port = None
        username = None
        password = None

        if '://' in proxy_string:
            scheme, proxy_string = proxy_string.split('://', 1)

        if '@' in proxy_string:
            creds, address = proxy_string.split('@')
            username, password = creds.split(':')
        else:
            address = proxy_string

        if scheme in ['socks4', 'socks4a', 'socks5', 'socks5h']:
            if scheme == 'socks4a':
                scheme = 'socks4'
                hostname = address
                port = 1080
            else:
                hostname, port = address.split(':', 1)
            if scheme == 'socks5h':
                scheme = 'socks5'
                hostname = address

        elif scheme in ['http', 'https']:
            hostname, port = address.split(':', 1)

        return {
                'scheme': scheme,
                'hostname': hostname,
                'port': int(port),
                'username': username,
                'password': password,
            }

    @classmethod
    def convert_proxy_to_json(cls, proxy_string: str) -> str:
        return json.dumps(cls.convert_proxy_to_dict(proxy_string))
