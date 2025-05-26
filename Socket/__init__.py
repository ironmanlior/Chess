#!/usr/bin/python

from __future__ import annotations
import socket, pickle, select, sys
from Compression import Compress, Decompress
from .message import Message
    

class Socket(socket.socket):
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, protocol=socket.IPPROTO_TCP, fileno=None):
        super().__init__(family=family, type=type, proto=protocol, fileno=fileno)
        self.buffersize = 10
        self.connections: list[socket.socket] = []
        self.game_types: dict[int, list[socket.socket]] = {}
        
    
    @classmethod
    def copy(cls, sock: socket.socket):
        return cls(sock.family, sock.type, sock.proto, fileno=socket.dup(sock.fileno()))
    
    def iter_accept(self) -> tuple[Socket, socket._RetAddress]:
        self.setblocking(False)
        for _ in select.select([self], [], [self], .05)[0]:
            conn, addr = super().accept()
            conn.setblocking(True)
            self.connections.append(conn)
            yield Socket.copy(conn), addr
    
    def accept(self) -> tuple[Socket, socket._RetAddress]:
        self.setblocking(False)
        conn, addr = super().accept()
        conn.setblocking(True)
        self.connections.append(conn)
        return Socket.copy(conn), addr
    
    def is_closed(self) -> bool:
        return self.fileno() == -1
    
    
    def send(self, data):
        @Compress
        def inner(data, freq):
            self.__send(data)
            self.__send(freq)
        # inner(data)
        self.__send(data)
    
    def __send(self, data):
        encode = pickle.dumps(data)
        length = f"{len(encode):<{self.buffersize}}".encode("utf-8")
        super().sendall(length + encode)
    
    def recv(self):
        @Decompress
        def inner():
            data = self.__recv()
            freq = self.__recv()
            return data, freq
        # return inner()
        return self.__recv()
    
    def __recv(self):
        try:
            length = int(super().recv(self.buffersize).decode("utf-8").strip())
            return pickle.loads(super().recv(length))
        except Exception as e:
            return None