from __future__ import annotations

class Node(object):
    def __init__(self, data: str, freq: int, left: Node=None, right: Node=None):
        self.data = data
        self.freq = freq
        self.left = left
        self.right = right
        
    def __add__(self, other: Node):
        return Node(f"{self.data}{other.data}", self.freq + other.freq, self, other)