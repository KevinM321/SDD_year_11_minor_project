import customer_functions
import loginscreen
import re
import shopscreen
from passlib.hash import pbkdf2_sha256

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.screenmanager import CardTransition

pattern = r'^[0-9]*$'


class ProfileScreenLayout(BoxLayout):

    @staticmethod
    def change_password():
        content = PasswordPopup()
        confirm_button = InterfaceButton(text='[b]Confirm[/b]')
        dismiss_button = InterfaceButton(text='[b]Cancel[/b]')
        content.change_password_footer.add_widget(confirm_button)
        content.change_password_footer.add_widget(dismiss_button)
        content.change_password_footer.add_widget(Label(size_hint_x=.2))
        popup = Popup(title='Change Password',
                      content=content,
                      size_hint=(.625, .625))
        confirm_button.bind(on_release=popup.dismiss)
        confirm_button.bind(on_release=content.confirm_password)
        dismiss_button.bind(on_release=popup.dismiss)
        popup.open()

    def card_info(self, args):
        popup = Popup(title='',
                      content=CardInfoPopup(),
                      size_hint=(.75, .75))
        popup.open()
        self.bound_card_info('')

    def logout(self):
        shopscreen.item_quantity.clear()
        self.screen_manager.transition = CardTransition(direction='down', mode='push')
        self.screen_manager.current = 'login_screen'

    @staticmethod
    def bound_card_info(args):
        if loginscreen.LoginScreenLayout.customer.details[3] != 'card number':
            CardInfoPopup.body.bound_card_number.text = ('**** **** **** ' +
                                                         loginscreen.LoginScreenLayout.customer.details[3][12:16])
        else:
            CardInfoPopup.body.bound_card_number.text = 'None'


class CardInfoPopup(BoxLayout):

    def __init__(self, **kwargs):
        super(CardInfoPopup, self).__init__(**kwargs)
        CardInfoPopup.body = self

    @staticmethod
    def bind_card_popup():
        confirm_button = InterfaceButton(text='[b]Confirm[/b]')
        dismiss_button = InterfaceButton(text='[b]Cancel[/b]')
        popup_content = CardPopup()
        popup_content.bind_card_popup_footer.add_widget(confirm_button)
        popup_content.bind_card_popup_footer.add_widget(dismiss_button)
        popup_content.bind_card_popup_footer.add_widget(Label(size_hint_x=.2))
        popup = Popup(title='',
                      content=popup_content,
                      size_hint=(.625, .625),
                      auto_dismiss=False)
        confirm_button.bind(on_release=popup.dismiss)
        confirm_button.bind(on_release=(lambda x: ProfileScreenLayout.bound_card_info('')))
        confirm_button.bind(on_release=popup_content.bind_card)
        dismiss_button.bind(on_release=popup.dismiss)
        popup.open()

    @staticmethod
    def unbind_card():
        if loginscreen.LoginScreenLayout.customer.details[3] == 'card number':
            popup = Popup(title='', content=Label(text='No bound card'), size_hint=(.5, .5))
        else:
            popup = Popup(title='', content=Label(text='Unbinding card successful'), size_hint=(.5, .5))
            card_info = ['card number', 'card pin', 'card expiration date']
            loginscreen.LoginScreenLayout.customer.update_account('', '', card_info, '')
            ProfileScreenLayout.bound_card_info('')
        popup.open()

    def successful_bind(self):
        Clock.schedule_once(lambda dt: self.card_image_change(), 0.25)
        Clock.schedule_once(lambda dt: self.card_image_change(), 1.5)

    def card_image_change(self):
        if self.card_image.source == 'res/Images/credit_card.png':
            self.card_image.source = 'res/Images/credit_card_confirmed.png'
        else:
            self.card_image.source = 'res/Images/credit_card.png'


class CardPopup(BoxLayout):

    def bind_card(self, args):
        if len(self.card_number.text) != 16 or not re.match(pattern, self.card_number.text):
            popup = Popup(title='',
                          content=Label(text='Invalid card number, must be 16 digits'),
                          size_hint=(.5, .5))
            popup.open()
        elif ((len(self.card_pin.text) < 3 or len(self.card_pin.text) > 4) or not
              re.match(pattern, self.card_pin.text)):
            popup = Popup(title='',
                          content=Label(text='Invalid card pin, must be 3 or 4 digits'),
                          size_hint=(.5, .5))
            popup.open()
        elif (len(self.card_date.text) != 2 or
              len(self.card_month.text) != 2 or
              len(self.card_year.text) != 2 or not
              re.match(pattern, self.card_date.text) or not
              re.match(pattern, self.card_month.text) or not
              re.match(pattern, self.card_year.text)):
            popup = Popup(title='',
                          content=Label(text='Invalid expiration date, all must be 2 digits'),
                          size_hint=(.5, .5))
            popup.open()
        else:
            card_info = [self.card_number.text,
                         self.card_pin.text,
                         (self.card_date.text + '/' + self.card_month.text + '/' + self.card_year.text)]
            CardInfoPopup.body.successful_bind()
            loginscreen.LoginScreenLayout.customer.update_account('', '', card_info, '')


class ProfileLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(ProfileLayout, self).__init__(**kwargs)
        ProfileLayout.body = self

    def on_profile(self, args):
        self.username.text = loginscreen.LoginScreenLayout.customer.name
        self.join_date.text = str(loginscreen.LoginScreenLayout.customer.details[7])
        if loginscreen.LoginScreenLayout.customer.details[8]:
            self.regular_status.text = 'Regular'
        else:
            self.regular_status.text = 'Irregular'  # this is a joke
        if loginscreen.LoginScreenLayout.customer.details[2]:
            ProfileImage.body.male_profile('')
        else:
            ProfileImage.body.female_profile('')


class ProfileImage(Image):

    def __init__(self, **kwargs):
        super(ProfileImage, self).__init__(**kwargs)
        ProfileImage.body = self

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            pic_choice = BoxLayout(spacing=100)
            male_button = Button(text='Male')
            female_button = Button(text='Female')
            pic_choice.add_widget(male_button)
            pic_choice.add_widget(female_button)
            popup = ProfileImagePopup(title='Change Profile Pic',
                                      content=pic_choice,
                                      size_hint=(.45, .25))
            male_button.bind(on_release=self.male_profile)
            female_button.bind(on_release=self.female_profile)
            popup.open()

    def male_profile(self, args):
        self.source = 'res/Images/male_profile.png'
        ProfileImage.gender = True

    def female_profile(self, args):
        ProfileImage.gender = False
        self.source = 'res/Images/female_profile.png'


class InterfaceButton(Button):
    pass


class ProfileImagePopup(Popup):

    def on_dismiss(self, **kwargs):
        super(ProfileImagePopup, self).on_dismiss(**kwargs)
        loginscreen.LoginScreenLayout.customer.update_account('', ProfileImage.gender, '', '')


class PasswordPopup(BoxLayout):

    def confirm_password(self, args):
        if self.old_password.text == '':
            popup = Popup(title='',
                          content=Label(text='Please input password'),
                          size_hint=(.5, .5))
            popup.open()
        else:
            if pbkdf2_sha256.verify(self.old_password.text, loginscreen.LoginScreenLayout.customer.details[1]):
                if not re.match(customer_functions.pattern, self.new_password.text):
                    popup = Popup(title='',
                                  content=Label(text='New password incorrect syntax'),
                                  size_hint=(.5, .5))
                    popup.open()
                else:
                    loginscreen.LoginScreenLayout.customer.update_account(self.new_password.text, '', '', '')
            else:
                popup = Popup(title='',
                              content=Label(text='Old password incorrect'),
                              size_hint=(.5, .5))
                popup.open()
