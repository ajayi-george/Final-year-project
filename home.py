from kivymd.uix.screen import MDScreen

from kivy.lang import Builder


class HomeScreen(MDScreen):
    Builder.load_file("home.kv")

    def iamamethod(self):
        pass

    def useme(self):
        pass

    def pleaseGeorge(self):
        pass

    def lol(self):
        pass
