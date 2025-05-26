#!/usr/bin/python

import socket, pickle, select
from DB import User
from Socket import Socket, Message
from DataStructure import Queue

class Chat(object):
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=2107):
        self.socket = Socket()
        self.socket.setblocking(False)
        self.connections: dict[User, Socket] = {}
        
        try:
            self.socket.bind((host, port))
        except socket.error as e:
            print(e)
        self.socket.listen()
        
        players: list[Socket] = [self.socket]
        
        while True:
            for sock in select.select(players, [], [], .05)[0]:
                sock: Socket = sock
                if sock == self.socket:
                    conn, addr = self.socket.accept()
                    user = conn.recv()
                    conn.setblocking(False)
                    self.connections[user] = conn
                    players.append(conn)
                else:
                    try:
                        message: Message = sock.recv()
                        self.connections[message.receiver].send(message)
                    except Exception as e:
                        players.remove(sock)
                        self.connections.pop(list(self.connections.keys())[list(self.connections.values()).index(sock)])
                    
                        
if __name__ == '__main__':
    Chat()