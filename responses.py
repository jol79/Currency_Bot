import requests
import pprint
import datetime
import os

from matplotlib import pyplot as plt 


"""
To get the list of the latest foreign exchange rates
GET /latest
To 
GET /latest?symbols=USD,GBP
"""
base_url = 'https://api.exchangeratesapi.io/'
end_path_latest = 'latest'


def default_response(user_input):
    message = str(user_input).lower()

    return "Choose options from the list of available commands"


def list_response():
    end_point = f'{base_url}{end_path_latest}'
    result = requests.get(end_point)

    result_dict = {}

    data = result.json()
    data['rates']

    for key, value in data['rates'].items():
        result_dict[key] = data['rates'][key]

    return(result_dict)


# a result of exchange
def exchange_response(currency, amount):
    end_point = f'{base_url}{end_path_latest}'

    given_currency = currency
    end_path_exchange = f'latest?symbols={given_currency}&base=USD'

    end_point = f'{base_url}{end_path_exchange}'

    result = requests.get(end_point)

    _currency = []
    exchange_rate = []

    data = result.json()
    data['rates']

    for key, value in data['rates'].items():
        exchange_rate.append(data['rates'][key])
        _currency.append(key)

    rate = exchange_rate[0]

    return int(amount) * rate


def history_response(currency):
    _base = 'USD'
    _currency = currency
    date_until = datetime.datetime.now().strftime('%Y-%m-%d')
    date_start = datetime.timedelta(days=7)
    date_from = (datetime.datetime.now() - date_start).strftime('%Y-%m-%d')

    history_period = f'{base_url}history?start_at={date_from}&end_at={date_until}&symbols={_currency}&base={_base}'

    history_result = requests.get(history_period)

    """
    keys - date
    values - exchange rate
    """
    date = []
    _exchange_rate = []
    _result = history_result.json()

    for key, value in _result['rates'].items():
        _exchange_rate.append(_result['rates'][key])
        date.append(key)

    _exchange_rate_keys = []
    _exchange_rate_value = []

    for data in _exchange_rate:
        for key, value in data.items():
            _exchange_rate_keys.append(key)
            _exchange_rate_value.append(value)

    exchange_rate_result = zip(date, _exchange_rate_value)

    """ Building graph with Matplotlib """
    fig = plt.figure()

    plt.plot(date, _exchange_rate_value, '-ob')
    plt.title(f"{_currency}/{_base} trend in time range {date_from} to {date_until}")
    plt.legend([f'{_currency}'])

    plot_name = f"{_currency} {_base} trend in time range {date_from} to {date_until}.png"

    fig.savefig(plot_name)
    return plot_name


