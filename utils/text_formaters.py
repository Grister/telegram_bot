from prettytable import PrettyTable


def format_currency_data(data):
    table = PrettyTable()
    table.field_names = ["Source", "Rate", "Buy", "Sell"]

    for source, rates in data.items():
        for rate in rates:
            table.add_row([source, rate['rate'], rate['buy'], rate['sell']])

    return f"<pre>{table.get_string()}</pre>"
