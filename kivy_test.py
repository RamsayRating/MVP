from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout

class InputScreen(Screen):
    pass

class TestApp(App):
    def build(self):
        #return Button(text='Hello World')
        return InputScreen()
        #pass
TestApp().run()
