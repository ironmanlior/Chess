from .node import Node

class Stack(object):
    def __init__(self):
        self.head = Node("head")
        self.size = 0
 
    # String representation of the stack
    def __str__(self):
        current = self.head.next
        out = ""
        while current != None:
            out += f"{current.value}\n"
            current = current.next
        return out
    
    def to_list(self):
        current = self.head.next
        out = []
        while current != None:
            out.insert(0, current.value)
            current = current.next
        return out
    
    # Get the current size of the stack
    def getSize(self) -> int:
        return self.size
 
    # Check if the stack is empty
    def isEmpty(self) -> bool:
        return self.size == 0
    
    def Clear(self) -> None:
        self.head.next = None
    
    def peek(self):
        if self.isEmpty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value
 
    # Push a value into the stack.
    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1
 
    # Remove a value from the stack and return.
    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value