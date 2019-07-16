from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


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
                      content=CardPopup())
        popup.open()


class CardPopup(BoxLayout):
    pass
