from kivy.clock import Clock
from random import randint

from shopscreen import item_data, item_quantity

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image


class LuckyDrawScreenLayout(BoxLayout):
    t = 0
    chance = True

    def __init__(self, **kwargs):
        super(LuckyDrawScreenLayout, self).__init__(**kwargs)
        self.event = 0

    def change_display(self):
        item = item_data[randint(0, 9)]
        self.lucky_draw_display.source = item[3]
        if self.t < 2:
            self.t += 0.2
        else:
            Clock.unschedule(self.event)
            self.lucky_draw_layout.clear_widgets()
            for item in item_quantity:
                pass
            self.lucky_draw_layout.add_widget(Label(text='Lucky draw used\n\nCome back next week for more',
                                                    halign='center'))
            popup = BoxLayout(orientation='vertical')
            popup.add_widget(Label(text=("You've drawn " + item[0]+' !')))
            popup.add_widget(Image(source=item[3]))
            popup.add_widget(Label(text='Come back next week for more!'))
            p = Popup(title='',
                      content=popup,
                      size_hint=(.5, .5))
            p.open()

    def lucky_draw(self):
        if LuckyDrawScreenLayout.chance:
            self.event = Clock.schedule_interval(lambda dt: self.change_display(), 0.2)
            LuckyDrawScreenLayout.chance = False
        else:
            popup = Popup(title='',
                          content=Label(text='Come back next week for more!'),
                          size_hint=(.5, .5))
            popup.open()


class LuckyDrawImage(Image):

    def __init__(self, **kwargs):
        super(LuckyDrawImage, self).__init__(**kwargs)


class LuckyDrawBox(BoxLayout):
    pass
