from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from ...Widgets.TimeSetter import GameTime
from ...Popup.Loading import Loading
from ...network import Network
from ...session import session

class GameMenu(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading: MDDialog = None
        self.expansion_panel = MDExpansionPanel(
            content = GameTime(self.expansion_panel.close_panel).start(),
            panel_cls = MDExpansionPanelOneLine(text="00:00")
        )
        Clock.schedule_interval(lambda x: self.update(), .0000001)
    
    def on_enter(self):
        self.ids.expansion_panel.add_widget(self.expansion_panel)
    
    def update(self):
        global session
        self.expansion_panel.panel_cls.text = ":".join(f"{session['gametime']}".split(":")[1:]) if session['gametime'].days == 0 else f"{session['gametime'].days} day(s)"
    
    def submit(self):
        global session
        session["client"] = Network()
        session["client"].connect()
        if not self.loading:
            self.loading = MDDialog(type="custom", size_hint=(None, None), content_cls=Loading(cancel=lambda x: self.dismiss_popup()))
        self.loading.open()
    
    def dismiss_popup(self):
        if self.loading:
            self.loading.dismiss()
            self.loading: MDDialog = None
            self.parent.current = "game"