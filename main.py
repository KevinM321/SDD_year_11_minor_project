from kivy.config import Config
Config.set('graphics', 'resizable', False)

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

# building each screen
Builder.load_file('loginscreen.kv')
Builder.load_file('shopscreen.kv')
Builder.load_file('cartscreen.kv')
Builder.load_file('luckydrawscreen.kv')
Builder.load_file('profilescreen.kv')


# screen manager class used for managing all the screens
class EMScreenManager(ScreenManager):

    # called when screen changes
    def on_current(self, instance, value):
        super(EMScreenManager, self).on_current(self, value)
        # if current is cart screen then call the display function, passing through item_quantity and item_data
        if value == 'cart_screen':
            CartLayout.display(item_quantity, item_data)
        # if current is profile screen call the on_profile function
        elif value == 'profile_screen':
            ProfileLayout.body.on_profile('args')
        # if current is lucky draw screen call the on_screen funcion
        elif value == 'lucky_draw_screen':
            LuckyDrawScreenLayout.body.on_screen()


# class for instance of the energy max app
class EnergyMaxApp(App):

    def build(self):
        return EMScreenManager()


# running the app
home = EnergyMaxApp()
home.run()
