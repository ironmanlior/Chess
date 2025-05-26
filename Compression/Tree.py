from .Node import Node

class Tree(object):
    def __new__(cls, data: str):
        self = super().__new__(cls)
        self.__init__(data)
        return self.tree, self.frequency
    
    def __init__(self, data: str):
        self.data = data
        self.list = []
        self.frequency = {}
        self.__get_frequency()
        self.__create_node_list()
        self.list.sort(key=lambda x: x.freq)
        while len(self.list) > 1:
            self.list[0] = self.list[0] + self.list.pop(1)
            self.list.sort(key=lambda x: x.freq)
        self.tree = self.list[0]
    
    @classmethod
    def rebuild(cls, frequency: dict):
        self = super().__new__(cls)
        self.list = []
        self.frequency = frequency
        self.__create_node_list()
        self.list.sort(key=lambda x: x.freq)
        while len(self.list) > 1:
            self.list[0] = self.list[0] + self.list.pop(1)
            self.list.sort(key=lambda x: x.freq)
        self.tree = self.list[0]
        return self.tree
    
    def __get_frequency(self):
        for ch in self.data:
            self.frequency[ch] = self.data.count(ch)

    def __create_node_list(self):
        for ch, freq in self.frequency.items():
            self.list.append(Node(ch, freq))
    