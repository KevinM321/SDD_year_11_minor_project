def discount(regular_status, order):
    discount_rate = 0
    if regular_status:
        discount_rate -= 0.05
    if order >= 250:
        discount_rate -= 0.1
    return discount_rate




