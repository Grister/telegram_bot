def format_currency_data(data: dict) -> str:
    row = ''
    try:
        for source, rates in data.items():
            row += f"<b>{source.upper()}</b> \n"

            for rate in rates:
                row += f"{rate['rate']}:  {rate['buy']}/{rate['sell']} \n"
            row += '\n'
    except Exception:
        row = 'To many requests. Please try later'
    return row
