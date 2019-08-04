# called to calculate the discount for the logged in customer according to that customer's paid time
def discount_method(regular_status):
    discount_rate = 1
    if regular_status >= 3:
        discount_rate -= 0.05
    return discount_rate
