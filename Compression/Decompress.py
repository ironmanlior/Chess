import pickle, codecs
from typing import Iterator
from .Node import Node
from .Tree import Tree

def toObject(a: str):
    # obj = a.encode()
    # obj = codecs.decode(obj, 'base64')
    # obj = pickle.loads(obj)
    return pickle.loads(bytes(a, "latin1"))

class Decompress(object):
    def __init__(self, func):
        self.func = func
        self.data = ""
    
    def __call__(self, *args, **kwargs):
        encode, freq = self.func(*args, **kwargs)
        return self.decompress(encode, freq)

    def decompress(self, encode: bytes, freq: dict):
        self.tree = Tree.rebuild(freq)
        encode = encode.decode("utf-8")
        length = len(encode)
        encoded = iter(encode)
        
        for _ in range(length):
            self.data += self.__decode_char(self.tree, encoded)
        return toObject(self.data)
    
    def __decode_char(self, node: Node, encoded: Iterator[str]):
        if node.left and node.right and len(node.data) > 1:
            try:
                bit = next(encoded)
                if bit == "0":
                    return self.__decode_char(node.left, encoded)
                elif bit == "1":
                    return self.__decode_char(node.right, encoded)
            except Exception as e:
                pass
        return node.data
    