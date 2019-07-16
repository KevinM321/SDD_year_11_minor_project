from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button


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
    def bind_card():
        popup = Popup(title='',
                      content=CardPopup(),
                      size_hint=(.625, .625))
        popup.open()


class CardPopup(BoxLayout):
    pass


class ProfileLayout(BoxLayout):
    pass


class ProfileImage(Image):

    def __init__(self, **kwargs):
        super(ProfileImage, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            pic_choice = BoxLayout(spacing=100)
            pic_choice.add_widget(Button(text='Male', size_hint=(.7, .3)))
            pic_choice.add_widget(Button(text='Female', size_hint=(.7, .3)))
            popup = Popup(title='Change Profile Pic',
                          content=pic_choice,
                          size_hint=(.45, .25))
            popup.open()
