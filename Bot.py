import credentials as keys
import responses as rep
import os

from telegram.ext import *


# conversation handler status
CURRENCY = 0
VALUE = 1
HISTORY_CURRENCY = 0

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
    
    # write response from the user to the conversation handler [0]
    return CURRENCY


# CURRENCY state
def exchange_input_amount_USD(update, context):
    # a response that user give in first question
    context.user_data['currency'] = update.message.text.upper()

    update.message.reply_text("Give amount in USD...")
    # write response from the user to the conversation handler [1]
    return VALUE


# VALUE state
def exchange_command(update, context): 
    context.user_data['amount'] = update.message.text.upper()

    # result of exchanging
    response = rep.exchange_response(context.user_data['currency'], context.user_data['amount'])
    update.message.reply_text("{:.2f}".format(response))
    return ConversationHandler.END


def history_input_give_currency(update, context):
    update.message.reply_text("Provide currency to see the history in format e.g.'CAD'...")
    
    # write response from the user to the conversation handler [0]
    return HISTORY_CURRENCY


def history_command(update, context):
    currency = update.message.text.upper()

    # contains the path to the image of a graph
    response = rep.history_response(currency)
    context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open(response, 'rb'))

    if os.path.exists(response):
        os.remove(response)
    else: 
        pass

    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("I hope the information was helpful")
    return ConversationHandler.END


conversation_handler_exchange = ConversationHandler(
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


conversation_handler_history = ConversationHandler(
    entry_points=[
        CommandHandler('history', history_input_give_currency)],
    
        states = {
            HISTORY_CURRENCY: [MessageHandler(Filters.text, history_command)]},
        
        fallbacks = [CommandHandler('stop', stop)]
)


def main():
    updater = Updater(keys.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('list', list_command))
    dp.add_handler(conversation_handler_exchange)
    dp.add_handler(conversation_handler_history)
    dp.add_handler(CommandHandler('help', help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling() # check all the time for the message
    updater.idle()


main()


