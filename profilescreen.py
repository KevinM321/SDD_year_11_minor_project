from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
# from kivy.uix.image import Image


class ProfileScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(ProfileScreenLayout, self).__init__(**kwargs)

    def change_password(self):
        pass

    @staticmethod
    def card_info():
        popup = Popup(title='',
                      content=CardPopup(),
                      size_hint=(.75, .75))
        popup.open()


class CardPopup(BoxLayout):
    pass
