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

# pattern for number input check
pattern = r'^[0-9]*$'


# cart screen layout for the whole cart screen
class CartScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(CartScreenLayout, self).__init__(**kwargs)
        CartScreenLayout.body = self

    # pay method when pay button pressed, create a popup
    @staticmethod
    def pay():
        # if total needed is 0, create popup
        if CartLayout.sum == 0:
            popup = Popup(title='',
                          content=Label(text='Your cart is empty, please add items first'),
                          size_hint=(.625, .625))
            popup.open()
        # else create a popup that includes 2 buttons for payment methods and input space for amount and address
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
            # when each button is pressed a different method is called
            cash_button.bind(on_release=lambda x: CartScreenLayout.cash_popup(content.pay_amount.text_input.text,
                                                                              content.address.text_input.text, False))
            card_button.bind(on_release=lambda x: CartScreenLayout.card_popup(content.pay_amount.text_input.text,
                                                                              content.address.text_input.text, True))
            popup.open()

    # method for clearing the item quantity dict and the cart display when clear cart button pressed
    @staticmethod
    def clear_cart():
        item_quantity.clear()
        CartLayout.display(item_quantity, item_data)

    # method called when cash button on pay popup is pressed
    @staticmethod
    def cash_popup(amount, address, card_type):
        # test if address input is empty and create a popup
        if address == '':
            Popup(title='', content=Label(text='Please input address'), size_hint=(.575, .575)).open()
        # test to see if the pay amount can be converted to float
        else:
            try:
                # if convertible test if amount is smaller than the total needed and create popup
                if amount == '' or float(amount) < float(CartLayout.sum):
                    Popup(title='', content=Label(text='Insufficient fund'), size_hint=(.575, .575)).open()
                # else test if amount is bigger than the 10000 maximum then create popup
                elif float(amount) > 10000:
                    Popup(title='', content=Label(text='Exceeded maximum'), size_hint=(.575, .575)).open()
                # else create a receipt popup.
                else:
                    content = ReceiptLayout()
                    # loop used for adding each bought item to the receipt
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
                    # test the card type boolean, if card button pressed it would be true and add a card number display
                    if card_type:
                        content.card_text.text = 'Card Number: '
                        content.card.text = '**** **** **** ' + LoginScreenLayout.customer.details[3][12:16]
                    # a row displaying amount of item bought and discount the customer has added to receipt
                    footer1 = ReceiptFooter()
                    footer1.number.text = str(CartLayout.item_count)
                    footer1.sum.text = str(round((1 - CartLayout.discount) * 100 +
                                                 CartLayout.additional_discount)) + '%'
                    footer1.left_name.text = 'Item count: '
                    footer1.right_name.text = 'Discount: '
                    content.add_widget(footer1)
                    # a row displaying total amount needed and the returned amount of money added to receipt
                    footer2 = ReceiptFooter()
                    footer2.right_box.spacing = 10
                    footer2.number.text = '  $' + str(round(CartLayout.sum, 1)) + '   '
                    footer2.sum.text = '$' + str(round(float(amount) - float(CartLayout.sum), 1))
                    footer2.left_name.text = 'Total: '
                    footer2.right_name.text = 'Returned:  '
                    content.add_widget(footer2)
                    # different details such as date, customer address and name of customer added to receipt
                    content.date.text = str(date.today())
                    content.receipt_address.text = address
                    print(LoginScreenLayout.customer.details[0])
                    content.receipt_name.text = LoginScreenLayout.customer.details[0]
                    # transaction data including all the customer details and receipt details packed into a list
                    transaction_data = [LoginScreenLayout.customer.details[0],
                                        LoginScreenLayout.customer.details[3],
                                        date.today(),
                                        address,
                                        CartLayout.item_count,
                                        round((1 - CartLayout.discount) * 100 +
                                              CartLayout.additional_discount),
                                        round(CartLayout.sum, 1),
                                        round(float(amount) - float(CartLayout.sum), 1)]
                    # transaction data saved into a pickle file
                    with open('receipts/transaction_data.p', 'ba') as f:
                        pickle.dump(transaction_data, f)
                    # create receipt popup, clear the shopping cart and update the number of times the customer paid
                    ReceiptPopup(title='Cash Receipt', content=content, size_hint=(.4, .85)).open()
                    LoginScreenLayout.customer.update_account('', '', '', '', '', 'paid')
                    CartScreenLayout.clear_cart()
            # if input amount is not convertible create popup
            except ValueError:
                Popup(title='', content=Label(text='Incorrect input'), size_hint=(.575, .575)).open()

    # method called when card button pressed.
    @staticmethod
    def card_popup(amount, address, card_type):
        # check if a bound card exists, if not create a popup
        if LoginScreenLayout.customer.details[3] == 'card number':
            Popup(title='', content=Label(text='No bound card'), size_hint=(.575, .575)).open()
        # if bound card does exist test if the card has expired or not
        else:
            # if expired create popup else call the cash popup method
            if datetime.strptime(LoginScreenLayout.customer.details[5], "%d/%m/%y").date() < (datetime.now()).date():
                Popup(title='', content=Label(text='Your card has expired'), size_hint=(.575, .575)).open()
            else:
                CartScreenLayout.cash_popup(amount, address, card_type)


# class for each instance of an item in cart layout
class CartItem(BoxLayout):

    name = StringProperty()
    price = NumericProperty()
    quantity = NumericProperty()
    overall = NumericProperty()

    # create self attributes
    def __init__(self, **kwargs):
        super(CartItem, self).__init__(**kwargs)
        self.name = kwargs.pop('name')
        self.quantity = kwargs.pop('quantity')
        self.price = kwargs.pop('price')


# a class for instance of the cart layout inside cart screen
class CartLayout(BoxLayout):
    # total sum of all cart item and item count of all the items
    sum = 0
    item_count = 0

    def __init__(self, **kwargs):
        super(CartLayout, self).__init__(**kwargs)
        CartLayout.cart = self

    # method called each time the screen changes to cart screen
    @staticmethod
    def display(item_quantities, items):  # item_quantities = item_quantity, items = item_data
        # discount method called to calculate a discount based on the customer's status
        CartLayout.discount = discount_method(LoginScreenLayout.customer.details[9])
        CartLayout.cart.clear_widgets()
        counter = 0
        CartLayout.additional_discount = 0
        # check item quantity dict is empty or not. if not creates a counter to check for each non-zero quantity item
        if item_quantities == {}:
            pass
        else:
            for item in item_quantities:
                if item_quantities[item][0] != 0 or item_quantities[item][1]:
                    counter += 1
        # if counter equal zero then cart is empty
        if counter == 0:
            CartLayout.cart.add_widget(Label(text='Your cart is empty'))
        # if not zero create and add cart item for each in item quantity into cart layout
        else:
            # using item in item quantities to extract info of the item from items
            for item in item_quantities:
                name, quantity, drawn = item, item_quantities[item][0], item_quantities[item][1]
                for i in items:
                    if name in i:
                        price = 0
                        # if the boolean drawn is true, then add a free one to that item in item quantity
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
            # if order more than 250 and customer is regular add another 10% discount
            if CartLayout.discount != 1:
                if CartLayout.sum > 250:
                    CartLayout.additional_discount += 10
                    CartLayout.sum = CartLayout.sum * (9/CartLayout.additional_discount)
        # display total amount, item count and total discount on cart screen
        CartScreenLayout.body.sum.text = '$' + str(round(CartLayout.sum, 1)) + '   '
        CartScreenLayout.body.item_count.text = '    ' + str(CartLayout.item_count)
        CartScreenLayout.body.discount.text = '  ' + str(round((1 - CartLayout.discount) * 100 +
                                                               CartLayout.additional_discount)) + '%'


# pay popup layout
class PayLayout(BoxLayout):
    pass


# receipt popup layout
class ReceiptLayout(BoxLayout):
    pass


# receipt popup footer layout
class ReceiptFooter(BoxLayout):
    pass


# class for instances of a receipt
class ReceiptPopup(Popup):

    # function called when the popup is dismissed
    def on_dismiss(self, **kwargs):
        super(ReceiptPopup, self).on_dismiss(**kwargs)
        # check how many receipts there are.
        with open('receipts/transaction_data.p', 'rb') as f:
            n = 0
            while True:
                try:
                    pickle.load(f)
                    n += 1
                except EOFError:
                    break
        # save the receipt data as a png with a number tag at the end so it won't be overwritten
        self.export_to_png(('receipts/receipt' + str(n)))


# class for instances of item in receipt
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
