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

    # currency = []
    # exchange_rate = []
    result_dict = {}

    data = result.json()
    data['rates']

    for key, value in data['rates'].items():
        # exchange_rate.append(data['rates'][key])
        # currency.append(key)
        result_dict[key] = data['rates'][key]

    # lst = zip(currency, exchange_rate)
    # for data in lst:
    #     update.message.reply_text(data)
    return(result_dict)

