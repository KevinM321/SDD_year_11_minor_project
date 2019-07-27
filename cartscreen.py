from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label


class CartScreenLayout(BoxLayout):

    def display_info(self):
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
        self.price = kwargs.pop('price')


class CartLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(CartLayout, self).__init__(**kwargs)
        CartLayout.cart = self

    @staticmethod
    def display(item_quantity, item_data):
        CartLayout.cart.clear_widgets()
        counter = 0
        for item in item_quantity:
            if item_quantity[item] != 0:
                counter += 1
        if counter == 0:
            CartLayout.cart.add_widget(Label(text='Your cart is empty'))
        else:
            for item in item_quantity:
                name, quantity = item, item_quantity[item]
                for i in item_data:
                    if name in i:
                        price = quantity * i[1]
                        break
                if quantity != 0:
                    CartLayout.cart.add_widget(CartItem(name=name,
                                                        quantity=quantity,
                                                        price=price))






