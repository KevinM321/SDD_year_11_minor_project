import Discount
import customer_functions

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import CardTransition


class LoginScreenLayout(BoxLayout):
    customer = ''

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

    def login(self):
        LoginScreenLayout.customer = customer_functions.Customer(self.usr_name_input.text, self.psw_input.text)
        msg = LoginScreenLayout.customer.check()
        if msg:
            popup = Popup(title='', content=Label(text=msg), size_hint=(.5, .5))
            popup.open()
        else:
            self.screen_manager.transition = CardTransition(direction='up', mode='pop')
            Discount.discount(msg, 0)
            self.screen_manager.current = 'shop_screen'

    def register(self):
        customer = customer_functions.Customer(self.usr_name_input.text, self.psw_input.text)
        popup = Popup(title='', content=Label(text=customer.register()), size_hint=(.5, .5))
        popup.open()


class MyButton(Button):
    pass


class PasswordMask(MyButton):

    def on_release(self):
        self.psw_input.password = not self.psw_input.password
        self.text = "Hide" if self.text == "Show" else "Show"
