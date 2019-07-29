from kivy.clock import Clock
from random import randint
from datetime import datetime

from shopscreen import item_data, item_quantity
from loginscreen import LoginScreenLayout

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image


class LuckyDrawScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(LuckyDrawScreenLayout, self).__init__(**kwargs)
        self.event = 0
        LuckyDrawScreenLayout.body = self

    def on_screen(self):
        if LoginScreenLayout.customer.details[7]:
            self.lucky_draw_layout.clear_widgets()
            self.lucky_draw_layout.add_widget(LuckyDrawImage())
        else:
            self.lucky_draw_layout.clear_widgets()
            self.lucky_draw_layout.add_widget(Label(text='Lucky draw used\n\nCome back next week for more',
                                                    halign='center'))

    def lucky_draw(self):
        if LoginScreenLayout.customer.details[7]:
            self.event = Clock.schedule_interval(lambda dt: LuckyDrawImage.body.change_display(), 0.2)
            LoginScreenLayout.customer.update_account('', '', '', datetime.today(), False, '')
        else:
            Popup(title='',
                  content=Label(text='Come back next week for more!'),
                  size_hint=(.5, .5)).open()


class LuckyDrawImage(Image):
    t = 0

    def __init__(self, **kwargs):
        super(LuckyDrawImage, self).__init__(**kwargs)
        self.source = 'res/Images/question_mark.png'
        LuckyDrawImage.body = self

    def change_display(self):
        item = item_data[randint(0, 9)]
        self.source = item[3]
        if self.t < 2:
            self.t += 0.2
        else:
            Clock.unschedule(LuckyDrawScreenLayout.body.event)
            LuckyDrawScreenLayout.body.lucky_draw_layout.clear_widgets()
            for item in item_quantity:
                pass
            LuckyDrawScreenLayout.body.lucky_draw_layout.add_widget(Label(text='Lucky draw used\n'
                                                                          '\nCome back next week for more',
                                                                          halign='center'))
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text=("You've drawn " + item[0]+' !')))
            content.add_widget(Image(source=item[3]))
            content.add_widget(Label(text='Come back next week for more!'))
            Popup(title='',
                  content=content,
                  size_hint=(.5, .5)).open()


class LuckyDrawBox(BoxLayout):
    pass
