from passlib.hash import pbkdf2_sha256
import pickle
import os
import re

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
                            regular_status = content[2]
                            return regular_status
                        return 'Incorrect password'
                except EOFError:
                    return 'Username not registered'

    def register(self):
        if self.name == '':
            return 'Username is empty'
        elif not re.match(pattern, self.name):
            return 'Username illegal'
        hash_brown = pbkdf2_sha256.hash(self.password)  # hashed password
        account = [self.name, hash_brown, False, 0]
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
