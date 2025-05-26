from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty, BooleanProperty

class Password(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    required = BooleanProperty()