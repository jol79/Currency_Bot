import requests
import pprint


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
    



