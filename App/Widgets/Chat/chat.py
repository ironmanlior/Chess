from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from App.session import session
from App.network import Network
from kivy.clock import Clock
from Socket import Message
import select

class MessageBox(MDLabel):
    def __init__(self, message: Message, **kwargs):
        global session
        self.message = message
        self.text = message.message
        self.is_sender = message.sender is session["user"]
        super().__init__(**kwargs)
        


class HistoryView(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self):
        Clock.schedule_interval(lambda x: self.recv(), .001)
    
    
    def recv(self):
        global session
        chat: Network = session["client"]
        for chat in select.select([chat.chat], [], [], .001)[0]:
            message: Message = chat.recvmsg()
            self.add_widget(MessageBox(message))
    
    def send(self, text):
        global session
        chat: Network = session["client"]
        message = Message(text, session["user"], session["rival"])
        chat.sendmsg(message)
        self.add_widget(MessageBox(message))
        
class Chat(MDScreen):
    def on_enter(self):
        global session
        session["client"].connect_chat()
    