from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


layout = FloatLayout(size=(300, 300))

button = Button(text='Hello world')
layout.add_widget(button)

button = Button(
    text='Hello world',
    size_hint=(.5, .25),
    pos=(20, 20))

button = Button(text='Hello world', size_hint=(.6, .6),pos_hint={'x':.2, 'y':.2})
