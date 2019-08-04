import customer_functions
from loginscreen import LoginScreenLayout
import re
import shopscreen
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.screenmanager import CardTransition

# pattern used for checking format of password input
pattern = r'^[0-9]*$'


# class for instance of profile screen
class ProfileScreenLayout(BoxLayout):

    # called when change password button pressed
    @staticmethod
    def change_password():
        content = PasswordPopup()
        # create and add confirm and dismiss buttons to the bottom of the change password popup
        confirm_button = InterfaceButton(text='[b]Confirm[/b]')
        dismiss_button = InterfaceButton(text='[b]Cancel[/b]')
        content.change_password_footer.add_widget(confirm_button)
        content.change_password_footer.add_widget(dismiss_button)
        content.change_password_footer.add_widget(Label(size_hint_x=.2))
        popup = Popup(title='Change Password',
                      content=content,
                      size_hint=(.625, .625),
                      auto_dismiss=False)
        confirm_button.bind(on_release=popup.dismiss)
        confirm_button.bind(on_release=content.confirm_password)
        dismiss_button.bind(on_release=popup.dismiss)
        popup.open()

    # called when card info button in profile screen is pressed
    def card_info(self, args):
        Popup(title='',
              content=CardInfoPopup(),
              size_hint=(.75, .75)).open()
        self.bound_card_info('')

    # called when logout button pressed
    def logout(self):
        # changes screen transition, changes screen and clear the item quantity dict
        shopscreen.item_quantity.clear()
        self.screen_manager.transition = CardTransition(direction='down', mode='push')
        self.screen_manager.current = 'login_screen'

    # called when card info pressed and popup opened
    @staticmethod
    def bound_card_info(args):
        # check and add the bound card number to card info popup
        if LoginScreenLayout.customer.details[3] != 'card number':
            CardInfoPopup.body.bound_card_number.text = ('**** **** **** ' +
                                                         ayout.customer.details[3][12:16])
        else:
            CardInfoPopup.body.bound_card_number.text = 'None'


# class for instances of the layout inside card info popup
class CardInfoPopup(BoxLayout):

    def __init__(self, **kwargs):
        super(CardInfoPopup, self).__init__(**kwargs)
        # saves the instance of card popup just opened
        CardInfoPopup.body = self

    # called when bind card button in card info popup is pressed
    @staticmethod
    def bind_card_popup():
        # create and add confirm and dismiss buttons to the bottom of the bind card popup
        confirm_button = InterfaceButton(text='[b]Confirm[/b]')
        dismiss_button = InterfaceButton(text='[b]Cancel[/b]')
        # create an instance of card popup as the bind card popup layout
        popup_content = CardPopup()
        popup_content.bind_card_popup_footer.add_widget(confirm_button)
        popup_content.bind_card_popup_footer.add_widget(dismiss_button)
        popup_content.bind_card_popup_footer.add_widget(Label(size_hint_x=.2))
        popup = Popup(title='',
                      content=popup_content,
                      size_hint=(.625, .625),
                      auto_dismiss=False)
        # bind confirm and dismiss buttons to call other functions when pressed
        confirm_button.bind(on_release=popup.dismiss)
        confirm_button.bind(on_release=(lambda x: ProfileScreenLayout.bound_card_info('')))
        confirm_button.bind(on_release=popup_content.bind_card)
        dismiss_button.bind(on_release=popup.dismiss)
        popup.open()

    # called when unbind card button in card info popup is pressed
    @staticmethod
    def unbind_card():
        # check if there is actually a bound card
        if LoginScreenLayout.customer.details[3] == 'card number':
            popup = Popup(title='', content=Label(text='No bound card'), size_hint=(.5, .5))
        else:
            popup = Popup(title='', content=Label(text='Unbinding card successful'), size_hint=(.5, .5))
            # call customer instance's update account function passing through the new card info
            card_info = ['card number', 'card pin', 'card expiration date']
            LoginScreenLayout.customer.update_account('', '', card_info, '', '', '')
            ProfileScreenLayout.bound_card_info('')
        popup.open()

    # called when a card gets bound successfully
    def successful_bind(self):
        # change the card image after a short period of time, then change back
        Clock.schedule_once(lambda dt: self.card_image_change(), 0.25)
        Clock.schedule_once(lambda dt: self.card_image_change(), 1.5)

    # called by successful bind
    def card_image_change(self):
        # change the card image in card info popup
        if self.card_image.source == 'res/Images/credit_card.png':
            self.card_image.source = 'res/Images/credit_card_confirmed.png'
        else:
            self.card_image.source = 'res/Images/credit_card.png'


# class for instances of card popup
class CardPopup(BoxLayout):

    # called when confirm button in bind card popup is pressed
    def bind_card(self, args):
        # check if all the inputs of the card(number, pin, expiration date) matches requirement
        if len(self.card_number.text_input.text) != 16 or not re.match(pattern, self.card_number.text_input.text):
            Popup(title='',
                  content=Label(text='Invalid card number, must be 16 digits'),
                  size_hint=(.5, .5)).open()
        elif ((len(self.card_pin.text_input.text) < 3 or len(self.card_pin.text_input.text) > 4) or not
              re.match(pattern, self.card_pin.text_input.text)):
            Popup(title='',
                  content=Label(text='Invalid card pin, must be 3 or 4 digits'),
                  size_hint=(.5, .5)).open()
        elif (len(self.card_date.text) != 2 or
              len(self.card_month.text) != 2 or
              len(self.card_year.text) != 2 or not
              re.match(pattern, self.card_date.text) or not
              re.match(pattern, self.card_month.text) or not
              re.match(pattern, self.card_year.text)):
            Popup(title='',
                  content=Label(text='Invalid expiration date, all must be 2 digits'),
                  size_hint=(.5, .5)).open()
        else:
            # if all correct call customer's update account function with new card if the card has not expired
            card_info = [self.card_number.text_input.text,
                         self.card_pin.text_input.text,
                         (self.card_date.text + '/' + self.card_month.text + '/' + self.card_year.text)]
            if (datetime.strptime(card_info[2], "%d/%m/%y")).date() < (datetime.now()).date():
                Popup(title='',
                      content=Label(text='Card already expired'),
                      size_hint=(.5, .5)).open()
            else:
                CardInfoPopup.body.successful_bind()
                LoginScreenLayout.customer.update_account('', '', card_info, '', '', '')


# class for profile layout instance inside profile screen
class ProfileLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(ProfileLayout, self).__init__(**kwargs)
        ProfileLayout.body = self

    # called when screen changes to profile screen
    def on_profile(self, args):
        # extract username, join date, gender and status from customer instance and assign each to profile screen
        self.username.text = LoginScreenLayout.customer.name
        self.join_date.text = str(LoginScreenLayout.customer.details[8])
        # status is determined by the amount of times the customer has paid, if more than three then its regular
        if LoginScreenLayout.customer.details[9] >= 3:
            self.regular_status.text = 'Regular'
        else:
            self.regular_status.text = 'Irregular'  # this is a joke
        # check what gender the customer is and change the profile image accordingly
        if LoginScreenLayout.customer.details[2]:
            ProfileImage.body.male_profile('')
        else:
            ProfileImage.body.female_profile('')


# class for the profile image in profile layout
class ProfileImage(Image):

    def __init__(self, **kwargs):
        super(ProfileImage, self).__init__(**kwargs)
        ProfileImage.body = self

    # called when itself is pressed
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # create a popup that allows the customer to choose what gender they are, therefore changing the pic
            pic_choice = BoxLayout(spacing=100)
            male_button = Button(text='Male')
            female_button = Button(text='Female')
            pic_choice.add_widget(male_button)
            pic_choice.add_widget(female_button)
            male_button.bind(on_release=self.male_profile)
            female_button.bind(on_release=self.female_profile)
            ProfileImagePopup(title='Change Profile Pic',
                              content=pic_choice,
                              size_hint=(.45, .25)).open()

    # change profile image to male when pressed
    def male_profile(self, args):
        self.source = 'res/Images/male_profile.png'
        ProfileImage.gender = True

    # change profile image to female when pressed
    def female_profile(self, args):
        ProfileImage.gender = False
        self.source = 'res/Images/female_profile.png'


# class for interface button
class InterfaceButton(Button):
    pass


# class for profile image popup
class ProfileImagePopup(Popup):

    # when itself is dismissed call the customer update account function to update gender
    def on_dismiss(self, **kwargs):
        super(ProfileImagePopup, self).on_dismiss(**kwargs)
        LoginScreenLayout.customer.update_account('', ProfileImage.gender, '', '', '', '')


# class for layout of change password popup
class PasswordPopup(BoxLayout):

    # called when confirm button in change password popup pressed
    def confirm_password(self, args):
        # check if old password matching or not
        if self.old_password.text_input.text == '':
            Popup(title='',
                  content=Label(text='Please input password'),
                  size_hint=(.5, .5)).open()
        # if matching and the new password format is correct call customer update account function for new password
        else:
            if pbkdf2_sha256.verify(self.old_password.text_input.text,
                                    LoginScreenLayout.customer.details[1]):
                if not re.match(customer_functions.pattern, self.new_password.text_input.text):
                    Popup(title='',
                          content=Label(text='New password incorrect syntax'),
                          size_hint=(.5, .5)).open()
                else:
                    LoginScreenLayout.customer.update_account(self.new_password.text_input.text, '', '', '', '', '')
            else:
                Popup(title='',
                      content=Label(text='Old password incorrect'),
                      size_hint=(.5, .5)).open()
