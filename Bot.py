import credentials as keys
import responses as rep

from telegram.ext import *


print("Bot initialized")


def start_command(update, context):
    update.message.reply_text('Choose anything from available options')


def help_command(update, context):
    update.message.reply_text('No support available in this Bot')


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = rep.default_response(text)

    update.message.reply_text(response)


def error(update, context):
    print(f'Update {update} caused error {context.error}')


def list_command(update, context):
    response = rep.list_response()
        
    for key, value in response.items():
        update.message.reply_text(key+" : "+str(value))


def exchange_command(update, context):
    pass    


def history_command(update, context):
    pass


def main():
    updater = Updater(keys.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('list', list_command))
    dp.add_handler(CommandHandler('exchange', exchange_command))
    dp.add_handler(CommandHandler('history', history_command))
    dp.add_handler(CommandHandler('help', help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling() # check all the time for the message
    updater.idle()


main()


