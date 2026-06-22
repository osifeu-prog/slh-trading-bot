def calculate_position_size(balance, risk_percent, entry_price, stop_loss_price):
    risk_amount = balance * (risk_percent / 100)
    risk_per_unit = abs(entry_price - stop_loss_price)
    if risk_per_unit == 0:
        return 0
    units = risk_amount / risk_per_unit
    return units
