from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from ...Popup.GameTime import GameTime
from ...session import session

class Menu(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog: MDDialog = None
    
    def open_dialog(self):
        self.content = GameTime(cancel=self.dismiss_popup)
        self.title = "pick game time"
        if not self.dialog:
            buttons=[
                MDRoundFlatButton(text="Cancel", on_release=self.dismiss_popup),
                MDRoundFlatButton(text=self.title, on_release=self.content.submit)
            ]
            self.dialog = MDDialog(title=self.title, type="custom", size_hint=(.7, None), content_cls=self.content, buttons=buttons)
        self.dialog.open()
    
    def dismiss_popup(self, obj):
        global session
        if self.dialog: self.dialog.dismiss()
        try:
            session["rival"]
            self.parent.current = "game"
        except Exception as e:
            pass
        