def net_profit_margin(net_profit, sales):
    """Net Profit Margin (%)"""

    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """Operating Profit Margin (%)"""

    if sales == 0:
        return None

    return (operating_profit / sales) * 100


def check_opm(calculated_opm, source_opm):

    if calculated_opm is None:
        return False

    return abs(calculated_opm - source_opm) > 1


def return_on_equity(net_profit, equity_capital, reserves):

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    operating_profit,
    interest,
    equity_capital,
    reserves,
    borrowings
):

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    ebit = operating_profit + interest

    return (ebit / capital) * 100


def return_on_assets(net_profit, total_assets):

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100
    