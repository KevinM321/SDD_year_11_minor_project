from shopscreen import item_quantity, item_data

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


class CartScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(CartScreenLayout, self).__init__(**kwargs)
        CartScreenLayout.body = self

    @staticmethod
    def pay():
        Popup().open()

    @staticmethod
    def clear_cart():
        item_quantity.clear()
        CartLayout.display(item_quantity, item_data)

    @staticmethod
    def help():
        content = ScrollView(size_hint=(.6, None))
        body = BoxLayout(orientation='vertical')
        body.bind(minimum_height=body.setter('height'))
        body.add_widget(Label(text='Hi'))
        body.add_widget(Label(text='Hi'))
        body.add_widget(Label(text='Hi'))
        body.add_widget(Label(text='Hi'))
        body.add_widget(Label(text='Hi'))
        content.add_widget(body)
        popup = Popup(title='Cart Screen Help', content=content, size_hint=(.625, .625))
        popup.open()


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
    def display(item_quantities, items):
        CartLayout.cart.clear_widgets()
        counter = 0
        sum = 0
        item_count = 0
        for item in item_quantities:
            if item_quantities[item] != 0:
                counter += 1
        if counter == 0:
            CartLayout.cart.add_widget(Label(text='Your cart is empty'))
        else:
            for item in item_quantities:
                name, quantity, drawn = item, item_quantities[item][0], item_quantities[item][1]
                for i in items:
                    if name in i:
                        price = quantity * i[1]
                        if drawn:
                            price -= i[1]
                            item_quantities[item][1] = False
                        sum += price
                        break
                item_count += quantity
                if quantity != 0:
                    CartLayout.cart.add_widget(CartItem(name=name,
                                                        quantity=quantity,
                                                        price=price))
        CartScreenLayout.body.sum.text = '$' + str(sum) + ' '
        CartScreenLayout.body.item_count.text = ' ' + str(item_count)






