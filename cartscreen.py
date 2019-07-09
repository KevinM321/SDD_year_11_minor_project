# from shopscreen import item_quantity

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty


class CartScreenLayout(BoxLayout):
    pass


class CartItem(BoxLayout):

    name = StringProperty()
    price = NumericProperty()
    quantity = NumericProperty()
    overall = NumericProperty()

    def __init__(self, **kwargs):
        super(CartItem, self).__init__(**kwargs)
        self.name = kwargs.pop('name')
        self.quantity = kwargs.pop('quantity')


class CartLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(CartLayout, self).__init__(**kwargs)

    def display(self, item_quantity):
        for item in item_quantity:
            name, quantity = item, item_quantity[item]
            self.add_widget(CartItem(name=name,
                                     quantity=quantity,
                                     size_hint_y=None,
                                     height=50))







