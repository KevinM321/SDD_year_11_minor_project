from shopscreen import item_quantity, item_data
from datetime import date, datetime
import pickle

from loginscreen import LoginScreenLayout
from Discount import discount_method

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

pattern = r'^[0-9]*$'


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
            popup.open()
        else:
            content = PayLayout()
            cash_button = Button(bold=True, text='Cash', size_hint_y=.45, size_hint_x=.6)
            card_button = Button(bold=True, text='Card', size_hint_y=.45, size_hint_x=.6)
            content.pay_footer.add_widget(Label(size_hint_x=.2, size_hint_y=.45))
            content.pay_footer.add_widget(cash_button)
            content.pay_footer.add_widget(Label(size_hint_x=.4, size_hint_y=.45))
            content.pay_footer.add_widget(card_button)
            content.pay_footer.add_widget(Label(size_hint_x=.2, size_hint_y=.45))
            popup = Popup(title='',
                          content=content,
                          size_hint=(.7, .7))
            cash_button.bind(on_release=popup.dismiss)
            card_button.bind(on_release=popup.dismiss)
            cash_button.bind(on_release=lambda x: CartScreenLayout.cash_popup(content.pay_amount.text_input.text,
                                                                              content.address.text_input.text, False))
            card_button.bind(on_release=lambda x: CartScreenLayout.card_popup(content.pay_amount.text_input.text,
                                                                              content.address.text_input.text, True))
            popup.open()

    @staticmethod
    def clear_cart():
        item_quantity.clear()
        CartLayout.display(item_quantity, item_data)

    @staticmethod
    def help():
        content = ScrollView(do_scroll_x=False)
        body = BoxLayout(orientation='vertical')
        # body.bind(minimum_height=body.setter('height'))
        content.add_widget(Label(text='something'))
        # content.add_widget(body)
        popup = Popup(title='Cart Screen Help', content=content, size_hint=(.625, .625))
        popup.open()

    @staticmethod
    def cash_popup(amount, address, card_type):
        if address == '':
            Popup(title='', content=Label(text='Please input address'), size_hint=(.575, .575)).open()
        else:
            try:
                if amount == '' or float(amount) < float(CartLayout.sum):
                    Popup(title='', content=Label(text='Insufficient fund'), size_hint=(.575, .575)).open()
                elif float(amount) > 10000:
                    Popup(title='', content=Label(text='Exceeded cash maximum'), size_hint=(.575, .575)).open()
                else:
                    content = ReceiptLayout()
                    for item in item_quantity:
                        name, quantity, drawn = item, item_quantity[item][0], item_quantity[item][1]
                        for i in item_data:
                            if name in i:
                                price = 0
                                if drawn:
                                    quantity += 1
                                    price -= i[1]
                                price += round(quantity * (i[1] * CartLayout.discount), 1)
                                break
                        if quantity != 0:
                            content.receipt_data.add_widget(ReceiptItem(name=name,
                                                                        quantity=quantity,
                                                                        price=price,
                                                                        pos_hint={'top': 1}))
                    if card_type:
                        content.card_text.text = 'Card Number: '
                        content.card.text = '**** **** **** ' + LoginScreenLayout.customer.details[3][12:16]
                    footer1 = ReceiptFooter()
                    footer1.number.text = str(CartLayout.item_count)
                    footer1.sum.text = str(round((1 - CartLayout.discount) * 100 +
                                                 CartLayout.additional_discount)) + '%'
                    footer1.left_name.text = 'Item count: '
                    footer1.right_name.text = 'Discount: '
                    footer2 = ReceiptFooter()
                    footer2.right_box.spacing = 10
                    footer2.number.text = '  $' + str(round(CartLayout.sum, 1)) + '   '
                    footer2.sum.text = '$' + str(round(float(amount) - float(CartLayout.sum), 1))
                    footer2.left_name.text = 'Total: '
                    footer2.right_name.text = 'Returned:  '
                    content.date.text = str(date.today())
                    content.receipt_address.text = address
                    content.add_widget(footer1)
                    content.add_widget(footer2)
                    transaction_data = [LoginScreenLayout.customer.details[0],
                                        LoginScreenLayout.customer.details[3],
                                        date.today(),
                                        address,
                                        CartLayout.item_count,
                                        round((1 - CartLayout.discount) * 100 +
                                              CartLayout.additional_discount),
                                        round(CartLayout.sum, 1),
                                        round(float(amount) - float(CartLayout.sum), 1)]
                    with open('receipts/transaction_data.p', 'ba') as f:
                        pickle.dump(transaction_data, f)
                    ReceiptPopup(title='Cash Receipt', content=content, size_hint=(.4, .85)).open()
                    LoginScreenLayout.customer.update_account('', '', '', '', '', 'paid')
                    CartScreenLayout.clear_cart()
            except ValueError:
                Popup(title='', content=Label(text='Incorrect cash input'), size_hint=(.575, .575)).open()
                return

    @staticmethod
    def card_popup(amount, address, card_type):
        if LoginScreenLayout.customer.details[3] == 'card number':
            Popup(title='', content=Label(text='No bound card'), size_hint=(.575, .575)).open()
        else:
            if datetime.strptime(LoginScreenLayout.customer.details[5], "%d/%m/%y").date() < (datetime.now()).date():
                Popup(title='', content=Label(text='Your card has expired'), size_hint=(.575, .575)).open()
            else:
                CartScreenLayout.cash_popup(amount, address, card_type)


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
        CartLayout.discount = discount_method(LoginScreenLayout.customer.details[9])
        CartLayout.cart.clear_widgets()
        counter = 0
        CartLayout.sum = 0
        CartLayout.item_count = 0
        CartLayout.additional_discount = 0
        if item_quantities == {}:
            pass
        else:
            for item in item_quantities:
                if item_quantities[item][0] != 0 or item_quantities[item][1]:
                    counter += 1
        if counter == 0:
            CartLayout.cart.add_widget(Label(text='Your cart is empty'))
        else:
            for item in item_quantities:
                name, quantity, drawn = item, item_quantities[item][0], item_quantities[item][1]
                for i in items:
                    if name in i:
                        price = 0
                        if drawn:
                            quantity += 1
                            price -= i[1]
                        price += round(quantity * (i[1] * CartLayout.discount), 1)
                        CartLayout.sum += price
                        break
                CartLayout.item_count += quantity
                if quantity != 0:
                    widget = CartItem(name=name,
                                      quantity=quantity,
                                      price=price)
                    CartLayout.cart.add_widget(widget)
            if CartLayout.discount != 1:
                if CartLayout.sum > 250:
                    CartLayout.additional_discount += 10
                    CartLayout.sum = CartLayout.sum * (9/CartLayout.additional_discount)
        CartScreenLayout.body.sum.text = '$' + str(round(CartLayout.sum, 1)) + '   '
        CartScreenLayout.body.item_count.text = '    ' + str(CartLayout.item_count)
        CartScreenLayout.body.discount.text = '  ' + str(round((1 - CartLayout.discount) * 100 +
                                                               CartLayout.additional_discount)) + '%'


class PayLayout(BoxLayout):
    pass


class ReceiptLayout(BoxLayout):
    pass


class ReceiptFooter(BoxLayout):
    pass


class ReceiptPopup(Popup):

    def on_dismiss(self, **kwargs):
        super(ReceiptPopup, self).on_dismiss(**kwargs)
        with open('receipts/transaction_data.p', 'rb') as f:
            n = 0
            while True:
                try:
                    pickle.load(f)
                    n += 1
                except EOFError:
                    break
        self.export_to_png(('receipts/receipt' + str(n)))


class ReceiptItem(BoxLayout):
    name = StringProperty()
    price = NumericProperty()
    quantity = NumericProperty()
    overall = NumericProperty()

    def __init__(self, **kwargs):
        super(ReceiptItem, self).__init__(**kwargs)
        self.name = kwargs.pop('name')
        self.quantity = kwargs.pop('quantity')
        self.price = kwargs.pop('price')
