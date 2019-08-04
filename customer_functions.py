from passlib.hash import pbkdf2_sha256
import pickle
import os
import re
from datetime import date

# pattern used to check for password and username input
pattern = r"[A-Za-z0-9]+$"


# class for instances of a logged in customer
class Customer:

    def __init__(self, name, password):
        self.name = name
        self.password = password

    # checking for correct username and password
    def check(self):
        if os.stat('Accounts.p').st_size == 0:
            return 'Please register'
        # check if username input is empty or not
        if not self.name:
            return 'Username is empty'
        # check if username exists or if password is correct or not
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

    # register function for new account
    def register(self):
        # check username format
        if self.name == '':
            return 'Username is empty'
        elif not re.match(pattern, self.name):
            return 'Username illegal'
        hash_brown = pbkdf2_sha256.hash(self.password)  # hashed password
        account = [self.name, hash_brown, True, 'card number', 'card pin',
                   'card expiration date', 'lucky_draw_date', True, date.today(), 0, 0]  # account details
        # check if file is empty and password format
        if os.stat('Accounts.p').st_size == 0:
            if self.password == '':
                return 'Password is empty'
            elif not re.match(pattern, self.password):
                return 'Password illegal'
            with open('Accounts.p', 'ba') as f:
                pickle.dump(account, f)
            return 'Successful registration'
        # check if username already exists or not
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
        # check password format
        if self.password == '':
            return 'Password is empty'
        elif not re.match(pattern, self.password):
            return 'Password illegal'
        with open('Accounts.p', 'ba') as f:
            pickle.dump(account, f)
            return 'Successful registration'

    # called to update the customer account with different parameters passed in
    @staticmethod
    def update_account(password, gender, card_info, lucky_draw_date, lucky_draw_chance, regular_status):
        if password:
            Customer.details[1] = pbkdf2_sha256.hash(password)
        if gender != '':
            Customer.details[2] = gender
        if lucky_draw_chance == False:
            Customer.details[7] = lucky_draw_chance
            Customer.details[6] = lucky_draw_date
        elif lucky_draw_chance == True:
            Customer.details[7] = lucky_draw_chance
        if regular_status:
            Customer.details[9] += 1
        if card_info:
            index = 2
            for item in card_info:
                index += 1
                Customer.details[index] = item
        accounts = list(Customer.unpickle_accounts('Accounts.p'))
        index = 0
        # finding the account corresponding to the customer logged in and update account for that person
        for i in accounts:
            if Customer.details[0] in i:
                break
            index += 1
        accounts[index] = Customer.details
        with open('Accounts.p', 'wb') as f:
            for i in accounts:
                pickle.dump(i, f)

    # used to create a list of all the accounts in the file
    @staticmethod
    def unpickle_accounts(file_name):
        with open(file_name, 'rb') as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    return
