import time
from random import randint

from kivy.uix.boxlayout import BoxLayout

items = ['res/Images/beef_jerky.png', 'res/Images/energy_max_bar.png',
         'res/Images/energy_max_protein_shake.png', 'res/Images/energy_max_supplement.png',
         'res/Images/energy_max_weightloss_shake.png', 'res/Images/gatorade_drink.png',
         'res/Images/gfuel_drink.png', 'res/Images/mixed_berries.png',
         'res/Images/non_fat_yogurt.png', 'res/Images/whey_protein.png']


class LuckyDrawScreenLayout(BoxLayout):

    def lucky_draw(self):
        t = 0
        while t < 3:
            self.lucky_draw_display.source = items[randint(0, 9)]
            time.sleep(0.3)
            t += 0.3





