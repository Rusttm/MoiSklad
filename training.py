# -*- coding: utf8 -*-
import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.widget import Widget

class MyGrid(Widget):
    pass

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()