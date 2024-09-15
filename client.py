import gevent
from gevent.socket import create_connection

class KeyValueStoreClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = create_connection((self.host, self.port))
        self.fileobj = self.socket.makefile('rw')

    def send_command(self, command):
        self.fileobj.write(command + "\n")
        self.fileobj.flush()
        return self.fileobj.readline().strip()

    def close(self):
        self.socket.close()

if __name__ == '__main__':
    client = KeyValueStoreClient()
    client.connect()
    print(client.send_command('SET key1 value1'))
    print(client.send_command('GET key1'))
    client.close()
