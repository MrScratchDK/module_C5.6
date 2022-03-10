import json

import requests
import telebot

TOKEN = '5161285973:AAFuvwPXcg5qonPQ6Q3mmcWFD9EeZj2cEEM'

bot = telebot.TeleBot(TOKEN)

keys = {'биткоин': "BTC",
        'эфириум': 'ETH',
        'доллар': 'USD',
        'рубль': 'RUB',
}

class ConvertionException(Exception):
    pass

class APIException:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту  {quote}!.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту  {base}!.')

        try:
            amount = float(amount)
        except KeyError:
            raise ConvertionException(f'Не удалось обработать количество  {amount}!.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

@bot.message_handler(commands=['start', 'help'])
def help(massage: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n /values увидеть список вех доступных валют"
    bot.reply_to(massage, text)

@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(massage, text)

@bot.message_handler(content_types=['text',])
def currency(massage: telebot.types.Message):
    try:
        values = massage.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров!')

        quote, base, amount = values
        total_base = APIException.convert( quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(massage, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(massage.chat.id, text)

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        text = json.loads(r.content)[keys[base]]

bot.polling()