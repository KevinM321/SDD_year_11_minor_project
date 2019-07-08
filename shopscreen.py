from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BoundedNumericProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.image import Image

item_data = (['Energy Max Bar', 3.50, 'Tastes good!', 'res/Images/energy_max_bar.png'],
             ['Non-Fat Yogurt', 7.00, 'Good for you!', 'res/Images/non_fat_yogurt.png'],
             ['Protein Shake', 14.00, 'Gain muscle!', 'res/Images/energy_max_protein_shake.png'],
             ['Weight Loss Shake', 14.00, 'Lose weight!', 'res/Images/energy_max_weightloss_shake.png'],
             ['Gatorade Sports Drink', 4.50, 'Hydration!', 'res/Images/gatorade_drink.png'],
             ['Beef Jerky', 5.50, 'Simply delicious!', 'res/Images/beef_jerky.png'],
             ['Mixed Berries', 4.50, 'Fruity!', 'res/Images/mixed_berries.png'],
             ['GFuel Energy', 45.50, 'Fuel yourself!', 'res/Images/gfuel_drink.png'],
             ['Whey Protein Powder', 57.00, 'Do you know the Whey?', 'res/Images/whey_protein.png'],
             ['Energy Max Supplement', 18.50, 'Healthy!', 'res/Images/energy_max_supplement.png'])


item_quantity = {}


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


class ImageButton(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            image_popup = Popup(title='',
                                content=Image(source=self.img_path),
                                size_hint=(.75, .75))
            image_popup.open()


class ItemLayout(GridLayout):

    def __init__(self, **kwargs):
        super(ItemLayout, self).__init__(**kwargs)
        for name, price, desc, img_path in item_data:
            self.add_widget(ItemButton(name=name,
                                       price=price,
                                       description=desc,
                                       img_path=img_path))
