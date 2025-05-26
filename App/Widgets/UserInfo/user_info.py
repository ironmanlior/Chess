from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty

class UserInfo(MDBoxLayout):
    user = ObjectProperty()
    username = StringProperty()
    color = StringProperty()
    rating = StringProperty()
    
    def update(self, user, color):
        self.user = user
        try:
            self.username = user.username
            self.rating = f"({user.rating})"
            self.ids.clock.start()
        finally:
            self.color = color
    