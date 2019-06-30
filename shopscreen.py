from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BoundedNumericProperty, NumericProperty
from kivy.uix.label import Label

item_data = (['Energy Max Bar', 3.50, 'Tastes good!', 'res/Images/energy_max_bar.png'],
             ['Non-Fat Yogurt', 6.50, '!', 'res/Images/energy_max_bar.png'],
             ['Protein Shake', 7.00, 'Tastes horrible but is good for you', 'res/Images/energy_max_protein_shake.png'],
             ['Weight Loss Shake', 7.00, 'Lose weight!', 'res/Images/energy_max_weightloss_shake.png'],
             ['Energy Max Bar', 3.50, 'Tastes good!', 'res/Images/energy_max_bar.png'],
             ['Energy Max Bar', 3.50, 'Tastes good!', 'res/Images/energy_max_bar.png'],
             ['Energy Max Bar', 3.50, 'Tastes good!', 'res/Images/energy_max_bar.png'])


item_quantity = {'k':1, 'e':2, 'v':3}


class InterfaceButton(Button):
    pass


class ShopScreenLayout(BoxLayout):
    pass


class ToolBarHeader(BoxLayout):
    pass


class ItemButton(RelativeLayout):

    name = StringProperty()
    price = NumericProperty()
    description = StringProperty()
    img_path = StringProperty()

    def __init__(self, **kwargs):
        super(ItemButton, self).__init__(**kwargs)
        self.name = kwargs.pop('name')
        self.price = kwargs.pop('price')
        self.description = kwargs.pop('description')
        self.img_path = kwargs.pop('img_path')

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            popup_layout = PopupLayout(name=self.name,
                                       price=self.price,
                                       description=self.description,
                                       img_path=self.img_path)
            popup_footer = BoxLayout()
            confirm_button = InterfaceButton(text="[b]Confirm[/b]")
            dismiss_button = InterfaceButton(text='[b]Cancel[/b]')
            popup_footer.add_widget(Label())
            popup_footer.add_widget(confirm_button)
            popup_footer.add_widget(Label())
            popup_footer.add_widget(dismiss_button)
            popup_footer.add_widget(Label())
            popup_layout.add_widget(popup_footer)
            item_popup = Popup(title=self.name,
                               content=popup_layout,
                               size_hint=(.6, .6),
                               auto_dismiss=False)
            dismiss_button.bind(on_release=item_popup.dismiss)
            dismiss_button.bind(on_release=popup_layout.clear)
            confirm_button.bind(on_release=item_popup.dismiss)
            confirm_button.bind(on_release=popup_layout.save)
            item_popup.open()
            return True
        else:
            return super(ItemButton, self).on_touch_up(touch)


class PopupLayout(BoxLayout):

    name = StringProperty()
    price = NumericProperty()
    description = StringProperty()
    img_path = StringProperty()
    quantity = BoundedNumericProperty(0, min=0, max=50)

    def __init__(self, **kwargs):
        super(PopupLayout, self).__init__(**kwargs)
        self.quantity = item_quantity.get(self.name, 0)

    def save(self, *args):
        item_quantity[self.name] = self.quantity

    def clear(self, *args):
        item_quantity[self.name] = 0


class ItemLayout(GridLayout):

    def __init__(self, **kwargs):
        super(ItemLayout, self).__init__(**kwargs)
        for name, price, desc, img_path in item_data:
            self.add_widget(ItemButton(name=name,
                                       price=price,
                                       description=desc,
                                       img_path=img_path))
