from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.uix.button import Button
from ....session import session
from Engine import Game

class MovesHistory(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
    
    def close_menu(self):
        pass
    
    def draw(self):
        pass
    
    def resign(self):
        pass
    
    
    def add_move(self):
        global session
        
        game: Game = session["game"]
        def return_to_move(instance):
            nonlocal game
            while instance != self.children[0]:
                self.undo_move()
            self.future.disabled = game.future.isEmpty()
            self.past.disabled = game.past.isEmpty()
        button = Button(
            text=f"{len(self.children) + 1}. {game.moves[len(self.children)]}",
            size_hint=(None, None),
            size=(self.size[0] / 2, self.parent.size[1] / 8),
            background_color=(0, 0, 0, 0)
        )
        button.bind(on_release=return_to_move)
        try:
            game.forward()
        except Exception as e:
            pass
        self.game()
        self.add_widget(button)
        self.future.disabled = game.future.isEmpty()
        self.past.disabled = game.past.isEmpty()
        
    
    def undo_move(self):
        global session
        game: Game = session["game"]
        if not game.past.isEmpty():
            try:
                game.backward()
                self.remove_widget(self.children[0])
            except Exception as e:
                pass
            self.game()
            self.future.disabled = game.future.isEmpty()
            self.past.disabled = game.past.isEmpty()
    
    def open_menu(self):
        menu_items = [
            {
                "viewclass": "OneLineIconListItem",
                "height": dp(40),
                "text": "draw",
                "valign": "center",
                "on_release": lambda x="draw": self.draw()
            },
            {
                "viewclass": "OneLineIconListItem",
                "height": dp(40),
                "text": "resign",
                "valign": "center",
                "on_release": lambda x="resign": self.resign()
            },
            {
                "viewclass": "OneLineIconListItem",
                "height": dp(40),
                "text": "rotate",
                "icon": "cached",
                "valign": "center",
                "on_release": lambda x="rotate": self.board.rotate()
            },
            
        ]
        menu = MDDropdownMenu(
            caller = self.root.ids.menu_button,
            items=menu_items,
            width_mult=4,
            position="bottom",
        )
        menu.check_position_caller(None, None, None)
        menu.open()