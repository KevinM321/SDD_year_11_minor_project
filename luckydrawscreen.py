from kivy.clock import Clock
from random import randint
from datetime import datetime

from shopscreen import item_data, item_quantity
from loginscreen import LoginScreenLayout

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image


# class for lucky draw screen
class LuckyDrawScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(LuckyDrawScreenLayout, self).__init__(**kwargs)
        # create a self variable and store an instance of self in the class
        self.event = 0
        LuckyDrawScreenLayout.body = self

    # called by main
    def on_screen(self):
        # check if the boolean value is true or not, if true clear lucky draw layout  and add the lucky draw image
        if LoginScreenLayout.customer.details[7]:
            self.lucky_draw_layout.clear_widgets()
            self.lucky_draw_layout.add_widget(LuckyDrawImage())
        # if not clear lucky draw layout and add a reminder
        else:
            self.lucky_draw_layout.clear_widgets()
            self.lucky_draw_layout.add_widget(Label(text='Lucky draw used\n\nCome back next week for more',
                                                    halign='center'))

    # called when start button pressed
    def lucky_draw(self):
        # if lucky draw chance boolean is true then schedule to call change_display every 0.1 second
        if LoginScreenLayout.customer.details[7]:
            self.event = Clock.schedule_interval(lambda dt: LuckyDrawImage.body.change_display(), 0.1)
            # call drawn_item to display a popup showing what you've drawn 0.5 second after change display stops
            Clock.schedule_once(lambda dt: LuckyDrawScreenLayout.drawn_item(), 2.05)
            # updating the draw time and draw chance to account
            LoginScreenLayout.customer.update_account('', '', '', datetime.today(), False, '')
        # if false pop up a reminder
        else:
            Popup(title='',
                  content=Label(text='Come back next week for more!'),
                  size_hint=(.5, .5)).open()

    # called by lucky_draw
    @staticmethod
    def drawn_item():
        # if item has not yet been added to cart, add it to cart with 0 quantity and true for drawn
        if item_quantity.get(LuckyDrawImage.item[0], '') == '':
            item_quantity[LuckyDrawImage.item[0]] = [0, True]
        # else change the boolean to true
        else:
            item_quantity[LuckyDrawImage.item[0]][1] = True


# class for lucky draw image in lucky draw layout
class LuckyDrawImage(Image):
    t = 0.4

    def __init__(self, **kwargs):
        super(LuckyDrawImage, self).__init__(**kwargs)
        # on initiation set it's source and saves an instance of itself
        self.source = 'res/Images/question_mark.png'
        LuckyDrawImage.body = self

    # called by lucky_draw
    def change_display(self):
        # choose an item and save it in the class
        LuckyDrawImage.item = item_data[randint(0, 9)]
        # change the images source
        self.source = LuckyDrawImage.item[3]
        # check time, if smaller than 2 second add 0.1, else stop the luck_draw scheduled event and create a popup
        if self.t < 2:
            self.t += 0.1
        else:
            Clock.unschedule(LuckyDrawScreenLayout.body.event)
            LuckyDrawScreenLayout.body.lucky_draw_layout.clear_widgets()
            LuckyDrawScreenLayout.body.lucky_draw_layout.add_widget(Label(text='Lucky draw used\n'
                                                                          '\nCome back next week for more',
                                                                          halign='center'))
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text=("You've drawn " + LuckyDrawImage.item[0]+' !')))
            content.add_widget(Image(source=LuckyDrawImage.item[3]))
            content.add_widget(Label(text='Come back next week for more!'))
            Popup(title='',
                  content=content,
                  size_hint=(.5, .5)).open()
