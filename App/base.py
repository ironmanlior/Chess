from kivymd.uix.boxlayout import MDBoxLayout
from DataStructure import Stack

class Base(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.past = Stack()
        self.current = "menu"
        self.future = Stack()
    
    def next_screen(self, x):
        if not self.future.isEmpty():
            self.past.push(self.current)
            self.current = self.future.pop()
        
    def prev_screen(self, x):
        if not self.past.isEmpty():
            self.future.push(self.current)
            self.current = self.past.pop()
