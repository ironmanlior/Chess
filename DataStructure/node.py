from __future__ import annotations

class Node(object):
    def __init__(self, value, next: Node = None):
        self.value = value
        self.next = next