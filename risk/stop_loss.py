def calculate_stop_loss(entry_price, atr, multiplier=2):
    return entry_price - (atr * multiplier)
