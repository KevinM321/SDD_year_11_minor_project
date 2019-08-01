def discount_method(regular_status):
    discount_rate = 1
    if regular_status >= 3:
        discount_rate -= 0.05
    return discount_rate
