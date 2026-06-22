def check_max_drawdown(current_equity, peak_equity, max_allowed_pct=20):
    if peak_equity == 0:
        return False
    drawdown = (peak_equity - current_equity) / peak_equity * 100
    return drawdown >= max_allowed_pct
