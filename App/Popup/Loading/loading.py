from kivymd.uix.boxlayout import MDBoxLayout
from ...session import session
from kivy.clock import Clock
import select

class Loading(MDBoxLayout):
    def __init__(self, cancel, **kwargs):
        super().__init__(**kwargs)
        self.cancel = cancel
        Clock.schedule_interval(self.check, 0.05)
    
    def check(self, x):
        global session
        try:
            session["rival"], session["color"], session["game"]
            if not session["rival"] or not session["color"] or not session["game"]:
                raise Exception("")
        except Exception as e:
            for socket in select.select([session["client"].client], [], [], .001)[0]:
                session["rival"], session["color"] = socket.recv()
                session["game"] = socket.recv()
                self.cancel(self)
                return False
        return True
    