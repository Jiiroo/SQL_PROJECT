from kivy.clock import Clock
from kivy.config import Config
from kivy.utils import rgba
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, NumericProperty
from libs.baseclass import login, lobby, scanner, db_conn, statistics, about
from kivy.core.window import Window

Window.fullscreen = False


class MyApp(MDApp):
    capacity = NumericProperty(20)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'You Trace Me'
        self.theme_cls.primary_palette = "Green"

    def build(self):
        kv_run = Builder.load_file("main.kv")
        return kv_run
        
    def colors(self, color_code):
        if color_code == 0:
            color_rgba = '#35353f'
        elif color_code == 1:
            color_rgba = '#09AF79'
        elif color_code == 2:
            color_rgba = '#ffffff'
        return rgba(color_rgba)

    def show_screen(self, name):
        self.root.current = 'login'
        self.root.get_screen('lobby').ids.manage.current = name
        return True


if __name__ == "__main__":

    MyApp().run()
