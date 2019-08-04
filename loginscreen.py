import customer_functions

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import CardTransition

from datetime import datetime


# class for layout of login screen
class LoginScreenLayout(BoxLayout):
    customer = ''

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

    # called when login button pressed
    def login(self):
        # create an instance of a customer using customer_functions and saves it as customer in LoginScreenLayout
        LoginScreenLayout.customer = customer_functions.Customer(self.usr_name_input.text_input.text,
                                                                 self.psw_input.psw_input.text_input.text)
        # use the Customer class function check() using username and password input
        msg = LoginScreenLayout.customer.check()
        # if login not successful create a popup containing the error message
        if msg:
            Popup(title='', content=Label(text=msg), size_hint=(.5, .5)).open()
        # else clear the login screen input box texts, change screen transition and screen
        else:
            self.screen_manager.transition = CardTransition(direction='up', mode='pop')
            self.usr_name_input.text_input.text = ''
            self.psw_input.psw_input.text_input.text = ''
            self.screen_manager.current = 'shop_screen'
            # check if a week has passed since last lucky draw, if so enable lucky draw
            if LoginScreenLayout.customer.details[6] != 'lucky_draw_date':
                date_now = datetime.now().date()
                drawn_date = LoginScreenLayout.customer.details[6].date()
                delta = date_now - drawn_date
                if delta.days >= 7:
                    LoginScreenLayout.customer.update_account('', '', '', '', True, '')

    # called when register button pressed
    def register(self):
        # create a customer instance and call the Customer register function
        customer = customer_functions.Customer(self.usr_name_input.text_input.text,
                                               self.psw_input.psw_input.text_input.text)
        Popup(title='', content=Label(text=customer.register()), size_hint=(.5, .5)).open()


class MyButton(Button):
    pass


# class for password show/hide button
class PasswordMask(MyButton):

    # on press show/hide password
    def on_release(self):
        self.psw_input.password = not self.psw_input.password
        self.text = "Hide" if self.text == "Show" else "Show"
