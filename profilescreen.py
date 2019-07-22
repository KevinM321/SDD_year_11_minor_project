from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label


class ProfileScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(ProfileScreenLayout, self).__init__(**kwargs)

    def change_password(self):
        pass

    @staticmethod
    def card_info():
        popup = Popup(title='',
                      content=CardInfoPopup(),
                      size_hint=(.75, .75))
        popup.open()


class CardInfoPopup(BoxLayout):

    def __init__(self, **kwargs):
        super(CardInfoPopup, self).__init__(**kwargs)

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
        dismiss_button.bind(on_release=popup.dismiss)
        popup.open()


class CardPopup(BoxLayout):
    pass


class ProfileLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(ProfileLayout, self).__init__(**kwargs)
        self.regular_status = 'Regular customer'
        self.join_date = '20/7/2019'


class ProfileImage(Image):

    def __init__(self, **kwargs):
        super(ProfileImage, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            pic_choice = BoxLayout(spacing=100)
            male_button = Button(text='Male')
            female_button = Button(text='Female')
            pic_choice.add_widget(male_button)
            pic_choice.add_widget(female_button)
            popup = Popup(title='Change Profile Pic',
                          content=pic_choice,
                          size_hint=(.45, .25))
            male_button.bind(on_release=self.male_profile)
            female_button.bind(on_release=self.female_profile)
            popup.open()

    def male_profile(self, args):
        self.source = 'res/Images/male_profile.png'

    def female_profile(self, args):
        self.source = 'res/Images/female_profile.png'


class InterfaceButton(Button):
    pass
