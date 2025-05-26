from Socket import Socket, Message
from .session import session

class Network(object):
    def __init__(self):
        self.client = Socket()
        self.chat = Socket()
        self.server = "192.168.68.67"
        self.user = None
    
    def connect(self):
        global session
        try:
            self.client.connect((self.server, 7949))
            self.user = session["user"]
            self.send(self.user)
            self.send(session["gametime"].total_seconds())
            self.client.setblocking(False)
        except Exception as e:
            raise Exception("connection error")
    
    def connect_chat(self):
        global session
        try:
            self.chat.connect((self.server, 2107))
            self.send(self.user)
        except Exception as e:
            raise Exception("connection error")
    
    def send(self, game1):
        self.client.send(game1)
    
    def sendmsg(self, message: Message): 
        self.chat.send(message)
    
    def recv(self): 
        return self.client.recv()
    
    def recvmsg(self) -> Message: 
        return self.chat.recv()
    
    def close(self):
        self.client.close()
        self.chat.close()
    