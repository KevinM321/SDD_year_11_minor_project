from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label

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
        CartLayout.cart = self

    @staticmethod
    def display(item_quantity):
        CartLayout.cart.clear_widgets()
        counter = 0
        for item in item_quantity:
            print(item_quantity[item])
            if item_quantity[item] != 0:
                counter += 1
        if counter == 0:
            CartLayout.cart.add_widget(Label(text='Your cart is empty'))
        else:
            for item in item_quantity:
                name, quantity = item, item_quantity[item]
                if quantity != 0:
                    CartLayout.cart.add_widget(CartItem(name=name,
                                                        quantity=quantity,
                                                        size_hint_y=None,
                                                        height=50))






