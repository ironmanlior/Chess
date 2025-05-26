from .node import Node
        
class Queue(object):
    def __init__(self):
        self.head = Node("head")
        self.tail: Node = self.head
        self.size = 0
        
    def Put(self, value):
        self.head = Node(value, self.head.next)
        self.size += 1
        
    def Pull(self):
        if self.size == 0:
            raise IndexError
        node = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        if self.size == 0:
            self.tail = self.head
        return node.value
    
    def Peek(self):
        if self.size == 0:
            raise IndexError
        return self.head.next.value
    
    def Size(self):
        return self.size