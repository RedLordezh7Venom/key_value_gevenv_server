import gevent
from gevent.server import StreamServer
from gevent.lock import Semaphore

class KeyValueStoreServer:
    def __init__(self, host = '127.0.0.1',port = 5000):
        self.data = {}
        self.lock = Semaphore()
        self.server = StreamServer((host,port),self.handle_client)
    
    def start(self):
        print("Server starting...")
        print("Status : 200 (OK)")
        self.server.serve_forever()

    def handle_client(self,socket,address):
        print(f"New connection from {address}")
        fileobj = socket.makefile('rw')
        while True:
            line = fileobj.readline()
            if not line:
                break
                command,*args = line.strip().split()
                response = self.handle_command(command,args)
                fileobj.write(reposnse + "\n")
                fileobj.flush()

    def handle_command(self,command,args):
        with self.lock:
            if command == 'SET':
                key,value = args
                self.data[key] = value
                return "200 OK"
            elif command == 'GET':
                key = args[0]
                return self.data.get(key,"404 Not Found")
            elif command == 'DELETE':
                key =args[0]
                return "200 OK" if self.data.pop(key,None) else "404 Not Found"
            elif command == 'FLUSH':
                self.data.clear()
                return "+OK"
            elif command == 'MGET':
                return str([self.data.get(key, "$-1") for key in args])
            elif command == 'MSET':
                for i in range(0, len(args), 2):
                    key, value = args[i], args[i+1]
                    self.data[key] = value
                return "200 OK"
            else:
                return "-ERROR: Unknown command"
            
if __name__ == '__main__':
    server = KeyValueStoreServer()
    server.start()
