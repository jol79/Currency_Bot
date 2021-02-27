import credentials as keys
import responses as rep

from telegram.ext import *


CURRENCY = 0
VALUE = 1

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
        update.message.reply_text(key+" : {:.2f}".format(value))


def exchange_input_give_currency(update, context):
    update.message.reply_text("Provide currency to exchange in format e.g.'CAD'...")
    
    # write response from the user to the conversation handler [1]
    return CURRENCY


# CURRENCY state
def exchange_input_amount_USD(update, context):
    # a response that user give in first question
    context.user_data['currency'] = update.message.text.upper()

    update.message.reply_text("Give amount in USD...")
    # write response from the user to the conversation handler [2]
    return VALUE


# VALUE state
def exchange_command(update, context): 
    context.user_data['amount'] = update.message.text.upper()

    # result of exchanging
    response = rep.exchange_response(context.user_data['currency'], context.user_data['amount'])
    update.message.reply_text("{:.2f}".format(response))
    return ConversationHandler.END


def history_command(update, context):
    pass


def stop(update, context):
    update.message.reply_text("I hope the information was helpful")
    return ConversationHandler.END


conversion_handler = ConversationHandler(
    # start point
    entry_points=[
        CommandHandler('exchange', exchange_input_give_currency)],
    
        # dict that will store the answers from the user
        states = {
            # read the answer for the first question (currency)
            CURRENCY: [MessageHandler(Filters.text, exchange_input_amount_USD)],
            # read the answer for the second question (USD amount to exchange)
            VALUE: [MessageHandler(Filters.text, exchange_command)]},
        
        # exit point
        fallbacks = [CommandHandler('stop', stop)]
)


def main():
    updater = Updater(keys.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('list', list_command))
    # dp.add_handler(CommandHandler('exchange', exchange_command))
    dp.add_handler(conversion_handler)
    dp.add_handler(CommandHandler('history', history_command))
    dp.add_handler(CommandHandler('help', help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling() # check all the time for the message
    updater.idle()


main()


