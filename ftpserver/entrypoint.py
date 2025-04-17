import signal
import sys
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class Server:
    def __init__(self, ip: str = '', port: int = 21):
        authorizer = DummyAuthorizer()
        authorizer.add_user(
            'infodengue',
            os.getenv("FTP_PASS"),
            '.',
            perm='elradfmwMT'
        )
        authorizer.add_anonymous("./guest/")

        handler = FTPHandler
        handler.authorizer = authorizer
        handler.banner = "Welcome to InfoDengue FTP Server"
        handler.passive_ports = range(30000, 31000)

        self.server = FTPServer((ip, port), handler)
        self.server.max_cons = 256
        self.server.max_cons_per_ip = 5

    def __call__(self):
        return self.server

    def serve_forever(self):
        return self.server.serve_forever()

    def close_all(self):
        return self.server.close_all()


def main():
    def shutdown(sig, frame):
        print("Shutting down...")
        server.close_all()
        sys.exit(0)

    server = Server()
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    server.serve_forever()


if __name__ == "__main__":
    main()
