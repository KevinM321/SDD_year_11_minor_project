from loginscreen import *
from shopscreen import *
from cartscreen import *
from profilescreen import *
from luckydrawscreen import *

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

kivy.require("1.10.1")

Window.clearcolor = .25, .25, .25, 1

Builder.load_file('loginscreen.kv')
Builder.load_file('shopscreen.kv')
Builder.load_file('cartscreen.kv')
Builder.load_file('luckydrawscreen.kv')
Builder.load_file('profilescreen.kv')


class EMScreenManager(ScreenManager):

    def on_current(self, instance, value):
        super(EMScreenManager, self).on_current(self, value)
        if value == 'cart_screen':
            CartLayout.display(item_quantity, item_data)
        if value == 'profile_screen':
            ProfileLayout.body.on_profile('args')
        if value == 'lucky_draw_screen':
            LuckyDrawScreenLayout.body.on_screen()


class EnergyMaxApp(App):

    def build(self):
        return EMScreenManager()


home = EnergyMaxApp()
home.run()
