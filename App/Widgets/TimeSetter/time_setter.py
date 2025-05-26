from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import timedelta
from ...session import session

class CustomTimeSetter(MDBoxLayout):
    def __init__(self, cancel, **kwargs):
        super().__init__(**kwargs)
        self.cancel = cancel
    
    def update(self, seconds, minutes):
        global session
        session["gametime"] = timedelta(seconds=seconds, minutes=minutes)


class GameTime(MDBoxLayout):
    def __init__(self, cancel, **kwargs):
        super().__init__(**kwargs)
        self.cancel = cancel
        self.expansion_panel = MDExpansionPanel(
            content = CustomTimeSetter(self.cancel_custom),
            panel_cls = MDExpansionPanelOneLine(text="00:00")
        )
    
    def start(self):
        self.expansion_panel.bind(on_open=lambda x: self.removes_marks_all_chips(None))
        self.ids.expansion_panel.add_widget(self.expansion_panel)
        return self
    
    def cancel_custom(self):
        self.expansion_panel.close_panel()
        self.cancel()
    
    def removes_marks_all_chips(self, selected):
        for chip in self.ids.timeless.children:
            if chip != selected:
                chip.active = False
        for chip in self.ids.lighting.children:
            if chip != selected:
                chip.active = False
        for chip in self.ids.daily.children:
            if chip != selected:
                chip.active = False
        for chip in self.ids.quick.children:
            if chip != selected:
                chip.active = False
        
        global session
        if selected:
            time: list[str] = selected.text.split(" ")
            if time[1] == "min":
                if time[0].find("|") != -1:
                    time = time[0].split("|")
                    session["gametime"] = timedelta(seconds=int(time[1]), minutes=int(time[0]))
                else:
                    session["gametime"] = timedelta(minutes=int(time[0]))
            elif time[1] in ["days", "day"]:
                session["gametime"] = timedelta(days=int(time[0]))
            self.cancel()