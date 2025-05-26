from kivymd.uix.button import MDRoundFlatButton
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from ...session import session
from ...Popup.Login import *

class Main(MDScreen):
    base = ObjectProperty()
    def __init__(self, **kwargs):        
        self.sign_in: MDDialog = None
        self.sign_up: MDDialog = None
        super().__init__(**kwargs)
        pass
        
    
    def on_enter(self):
        self.parent.parent.parent.parent.parent.parent.past.push(self.name)
        pass
    
    def open_sign_in(self):
        self.content = SignIn(cancel=self.dismiss_popup)
        self.title = "Sign-In"
        if not self.sign_in:
            buttons=[
                MDRoundFlatButton(text="Cancel", on_release=self.dismiss_popup),
                MDRoundFlatButton(text=self.title, on_release=self.content.submit)
            ]
            self.sign_in = MDDialog(title=self.title, type="custom", size_hint=(.9, None), content_cls=self.content, buttons=buttons)
        self.sign_in.open()
    
    def open_sign_up(self):
        self.content = SignUp(cancel=self.dismiss_popup)
        self.title = "Sign-Up"
        if not self.sign_up:
            buttons=[
                MDRoundFlatButton(text="Cancel", on_release=self.dismiss_popup),
                MDRoundFlatButton(text=self.title, on_release=self.content.submit)
            ]
            self.sign_up = MDDialog(title=self.title, type="custom", size_hint=(.9, None), content_cls=self.content, buttons=buttons)
        self.sign_up.open()
    
    def dismiss_popup(self, obj):
        global session
        if self.sign_up:
            self.sign_up.dismiss()
        elif self.sign_in:
            self.sign_in.dismiss()
        try:
            self.base.username = session["user"].username
            self.parent.current = "login"
        except Exception as e:
            pass
    
