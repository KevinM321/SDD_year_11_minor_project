from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BoundedNumericProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.image import Image

# data for each item the shop has
item_data = (['Energy Max Bar', 3.50, 'Tastes good!', 'res/Images/energy_max_bar.png'],
             ['Non-Fat Yogurt', 6.00, 'Good for you!', 'res/Images/non_fat_yogurt.png'],
             ['Protein Shake', 14.00, 'Gain muscle!', 'res/Images/energy_max_protein_shake.png'],
             ['Weight Loss Shake', 14.00, 'Lose weight!', 'res/Images/energy_max_weightloss_shake.png'],
             ['Gatorade Sports Drink', 4.50, 'Hydration!', 'res/Images/gatorade_drink.png'],
             ['Beef Jerky', 5.50, 'Simply delicious!', 'res/Images/beef_jerky.png'],
             ['Mixed Berries', 7.00, 'Fruity!', 'res/Images/mixed_berries.png'],
             ['GFuel Energy', 45.50, 'Fuel yourself!', 'res/Images/gfuel_drink.png'],
             ['Whey Protein Powder', 57.00, 'Do you know the Whey?', 'res/Images/whey_protein.png'],
             ['Energy Max Supplement', 18.50, 'Healthy!', 'res/Images/energy_max_supplement.png'])


# dict used for when items are being added to the shopping cart
item_quantity = {}


# button class for each screen's header and footer
class InterfaceButton(Button):
    pass


# shop screen
class ShopScreenLayout(BoxLayout):
    pass


# uniform header, every screen has the same
class ToolBarHeader(BoxLayout):
    pass


# button for each instance of an item in item data
class ItemButton(RelativeLayout):

    name = StringProperty()
    price = NumericProperty()
    description = StringProperty()
    img_path = StringProperty()
    quantity = BoundedNumericProperty(0, min=0, max=50)

    def __init__(self, **kwargs):
        super(ItemButton, self).__init__(**kwargs)
        self.name = kwargs.pop('name')
        self.price = kwargs.pop('price')
        self.description = kwargs.pop('description')
        self.img_path = kwargs.pop('img_path')
        self.quantity = item_quantity.get(self.name, [0, False])[0]

    # function called when button pressed
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            # create a popup and add different buttons, descriptions of the item into it.
            popup_layout = PopupLayout(name=self.name,
                                       price=self.price,
                                       description=self.description,
                                       img_path=self.img_path)
            popup_footer = BoxLayout()
            confirm_button = InterfaceButton(text="[b]Confirm[/b]")
            dismiss_button = InterfaceButton(text='[b]Clear[/b]')
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
            # adding confirm and dismiss button to item popup
            dismiss_button.bind(on_release=item_popup.dismiss)
            dismiss_button.bind(on_release=popup_layout.clear)
            confirm_button.bind(on_release=item_popup.dismiss)
            confirm_button.bind(on_release=popup_layout.save)
            item_popup.open()
            return True
        else:
            return super(ItemButton, self).on_touch_up(touch)


# class for each instance of item popup
class PopupLayout(BoxLayout):

    name = StringProperty()
    price = NumericProperty()
    description = StringProperty()
    img_path = StringProperty()
    quantity = BoundedNumericProperty(0, min=0, max=50)

    def __init__(self, **kwargs):
        super(PopupLayout, self).__init__(**kwargs)
        if item_quantity.get(self.name, 0) == 0:
            item_quantity[self.name] = [0, False]
            self.quantity = item_quantity[self.name][0]
        else:
            self.quantity = item_quantity.get(self.name)[0]

    # function called when confirm button in item popup pressed
    def save(self, *args):
        item_quantity[self.name][0] = self.quantity

    # function called when clear button in item popup pressed
    def clear(self, *args):
        item_quantity[self.name][0] = 0


# image button used in each item popup layout
class ImageButton(Image):

    # called when itself is pressed and popup a bigger image
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            image_popup = Popup(title='',
                                content=Image(source=self.img_path),
                                size_hint=(.75, .75))
            image_popup.open()


# layout for containing all the item buttons
class ItemLayout(GridLayout):

    def __init__(self, **kwargs):
        super(ItemLayout, self).__init__(**kwargs)
        for name, price, desc, img_path in item_data:
            button = ItemButton(name=name,
                                price=price,
                                description=desc,
                                img_path=img_path)
            self.add_widget(button)


# uniform footer appearance, but different screen has their own buttons for their functionality
class ToolBarFooter(BoxLayout):
    pass
