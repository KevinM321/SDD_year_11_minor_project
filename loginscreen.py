import customer_functions

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import CardTransition

from datetime import datetime


class LoginScreenLayout(BoxLayout):
    customer = ''

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

    def login(self):
        LoginScreenLayout.customer = customer_functions.Customer(self.usr_name_input.text_input.text,
                                                                 self.psw_input.psw_input.text_input.text)
        msg = LoginScreenLayout.customer.check()
        if msg:
            Popup(title='', content=Label(text=msg), size_hint=(.5, .5)).open()
        else:
            self.screen_manager.transition = CardTransition(direction='up', mode='pop')
            self.usr_name_input.text_input.text = ''
            self.psw_input.psw_input.text_input.text = ''
            self.screen_manager.current = 'shop_screen'
            if LoginScreenLayout.customer.details[6] != 'lucky_draw_date':
                date_now = datetime.now().date()
                drawn_date = LoginScreenLayout.customer.details[6].date()
                delta = date_now - drawn_date
                if delta.days >= 7:
                    LoginScreenLayout.customer.update_account('', '', '', '', True, '')

    def register(self):
        customer = customer_functions.Customer(self.usr_name_input.text_input.text,
                                               self.psw_input.psw_input.text_input.text)
        Popup(title='', content=Label(text=customer.register()), size_hint=(.5, .5)).open()


class MyButton(Button):
    pass


class PasswordMask(MyButton):

    def on_release(self):
        self.psw_input.password = not self.psw_input.password
        self.text = "Hide" if self.text == "Show" else "Show"
