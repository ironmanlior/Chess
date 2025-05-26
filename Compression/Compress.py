import pickle, codecs
from re import A
from .Node import Node
from .Tree import Tree


def toString(a) -> str:
    return str(pickle.dumps(a), encoding="latin1")

class Compress(object):
    def __init__(self, func):
        self.func = func
        self.encode = ""
    
    def __call__(self, data, *args, **kwargs):
        data1 = self.compress(data)
        return self.func(data1, self.freq, *args, **kwargs)
    
    def compress(self, data):
        self.data = toString(data)
        self.tree, self.freq = Tree(self.data)
        for ch in self.data:
            self.__encode_char(self.tree, ch)
        return self.encode.encode("utf-8")
    
    def __encode_char(self, node: Node, ch: str):
        if node.left and ch in node.left.data:
            self.encode += "0"
            return self.__encode_char(node.left, ch)
        elif node.right and ch in node.right.data:
            self.encode += "1"
            return self.__encode_char(node.right, ch)

    
