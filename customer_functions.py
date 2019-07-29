from passlib.hash import pbkdf2_sha256
import pickle
import os
import re
from datetime import date

# method one
# ALLOWED_CHAR = ascii_letters + "1234567890"
# print(all([c in ALLOWED_CHAR for c in "abckkk"]))


pattern = r"[A-Za-z0-9]+$"


class Customer:

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def check(self):
        if os.stat('Accounts.p').st_size == 0:
            return 'Please register'
        if not self.name:
            return 'Username is empty'
        with open('Accounts.p', 'br') as f:
            loop = True
            while loop:
                try:
                    content = pickle.load(f)
                    if self.name in content:
                        if pbkdf2_sha256.verify(self.password, content[1]):
                            Customer.details = content
                            return
                        return 'Incorrect password'
                except EOFError:
                    return 'Username not registered'

    def register(self):
        if self.name == '':
            return 'Username is empty'
        elif not re.match(pattern, self.name):
            return 'Username illegal'
        hash_brown = pbkdf2_sha256.hash(self.password)  # hashed password
        account = [self.name, hash_brown, True, 'card number', 'card pin',
                   'card expiration date', 'lucky_draw_date', True, date.today(), 0, 0]  # account details
        if os.stat('Accounts.p').st_size == 0:
            with open('Accounts.p', 'ba') as f:
                pickle.dump(account, f)
            return 'Successful registration'
        else:
            loop = True
            with open('Accounts.p', 'br') as f:
                while loop:
                    try:
                        content = pickle.load(f)
                        if self.name in content:
                            return 'Username already exist'
                    except EOFError:
                        break
        if self.password == '':
            return 'Password is empty'
        elif not re.match(pattern, self.password):
            return 'Password illegal'
        with open('Accounts.p', 'ba') as f:
            pickle.dump(account, f)
            return 'Successful registration'

    @staticmethod
    def update_account(password, gender, card_info, lucky_draw_date, lucky_draw_chance, regular_status):
        if password:
            Customer.details[1] = pbkdf2_sha256.hash(password)
        if gender != '':
            Customer.details[2] = gender
        if lucky_draw_chance == False:
            Customer.details[7] = lucky_draw_chance
            Customer.details[6] = lucky_draw_date
        if regular_status:
            Customer.details[8] += 1
        if card_info:
            index = 2
            for item in card_info:
                index += 1
                Customer.details[index] = item
        accounts = list(Customer.unpickle_accounts('Accounts.p'))
        index = 0
        for i in accounts:
            if Customer.details[0] in i:
                break
            index += 1
        accounts[index] = Customer.details
        with open('Accounts.p', 'wb') as f:
            for i in accounts:
                pickle.dump(i, f)

    @staticmethod
    def unpickle_accounts(file_name):
        with open(file_name, 'rb') as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    return
