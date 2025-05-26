#!/usr/bin/python
import kivy, os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
import App

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
kivy.require("2.0.0")
Config.set('graphics', 'multisamples', '0')
#Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class Main(MDApp):
    icon = "App/Media/chess_icon.ico"
    title = "Chess"
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "Brown"
        self.theme_cls.primary_hue = "A700"  # "500"
        self.theme_cls.primary_light_hue = "50"
        self.theme_cls.primary_dark_hue = "500"

        return Builder.load_file("./App/base.kv")

if __name__ == "__main__":
    Main().run()