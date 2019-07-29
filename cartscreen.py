from shopscreen import item_quantity, item_data
from datetime import date

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
# from kivy.lang import Builder


class CartScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(CartScreenLayout, self).__init__(**kwargs)
        CartScreenLayout.body = self

    @staticmethod
    def pay():
        if CartLayout.sum == 0:
            popup = Popup(title='',
                          content=Label(text='Your cart is empty, please add items first'),
                          size_hint=(.625, .625))
        else:
            content = PayLayout()
            cash_button = Button(bold=True, text='Cash', size_hint_y=.375, size_hint_x=.6)
            card_button = Button(bold=True, text='Card', size_hint_y=.375, size_hint_x=.6)
            content.pay_footer.add_widget(Label(size_hint_x=.2, size_hint_y=.375))
            content.pay_footer.add_widget(cash_button)
            content.pay_footer.add_widget(Label(size_hint_x=.4, size_hint_y=.375))
            content.pay_footer.add_widget(card_button)
            content.pay_footer.add_widget(Label(size_hint_x=.2, size_hint_y=.375))
            popup = Popup(title='',
                          content=content,
                          size_hint=(.7, .7))
            cash_button.bind(on_release=popup.dismiss)
            card_button.bind(on_release=popup.dismiss)
            cash_button.bind(on_release=lambda x: CartScreenLayout.cash_popup(content.pay_amount.text))
            card_button.bind(on_release=lambda x: CartScreenLayout.card_popup(content.pay_amount.text))
        popup.open()

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

    @staticmethod
    def cash_popup(amount):
        if float(amount) < float(CartLayout.sum):
            Popup(title='', content=Label(text='Insufficient fund'), size_hint=(0.625, 0.625)).open()
        else:
            content = ReceiptLayout()
            for item in item_quantity:
                name, quantity, drawn = item, item_quantity[item][0], item_quantity[item][1]
                for i in item_data:
                    if name in i:
                        price = quantity * i[1]
                        if drawn:
                            price -= i[1]
                            item_quantity[item][1] = False
                        break
                if quantity != 0:
                    content.receipt_data.add_widget(CartItem(name=name,
                                                             quantity=quantity,
                                                             price=price,
                                                             height=25,
                                                             spacing=40))
            footer = ReceiptFooter()
            footer.item_count.text = '     ' + str(CartLayout.item_count)
            footer.sum.text = '$' + str(CartLayout.sum) + ' '
            content.date.text = str(date.today())
            content.add_widget(footer)
            Popup(title='', content=content, size_hint=(.45, .75)).open()

    @staticmethod
    def card_popup(amount):
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
    sum = 0
    item_count = 0

    def __init__(self, **kwargs):
        super(CartLayout, self).__init__(**kwargs)
        CartLayout.cart = self

    @staticmethod
    def display(item_quantities, items):
        CartLayout.cart.clear_widgets()
        counter = 0
        CartLayout.sum = 0
        CartLayout.item_count = 0
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
                        CartLayout.sum += price
                        break
                CartLayout.item_count += quantity
                if quantity != 0:
                    CartLayout.cart.add_widget(CartItem(name=name,
                                                        quantity=quantity,
                                                        price=price))
        CartScreenLayout.body.sum.text = '$' + str(CartLayout.sum) + ' '
        CartScreenLayout.body.item_count.text = ' ' + str(CartLayout.item_count)


class PayLayout(BoxLayout):
    pass


class ReceiptLayout(BoxLayout):
    pass


class ReceiptFooter(BoxLayout):
    pass
