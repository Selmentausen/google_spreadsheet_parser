import os
import logging
from telegram.ext import Updater, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", '5655136236:AAHeKyqqIcolMiHGtp0mrsiJZq8wdeup-TY')

help_markup = ReplyKeyboardMarkup([['/status', '/help'], ['/currently_tracking']])
status_markup = ReplyKeyboardMarkup([['/track', '/currently_tracking']])
currently_tracking_markup = ReplyKeyboardMarkup([['/stop_tracking']])


def start_tracking(update, context):
    update.message.reply_text('Вы начали отслеживать заказ!', reply_markup=ReplyKeyboardRemove())


def stop_tracking(update, context):
    update.message.reply_text('Вы прекратили отслеживать заказ!', reply_markup=ReplyKeyboardRemove())


def currently_tracking(update, context):
    update.message.reply_text('Вот все заказы которые вы отслеживаете...', reply_markup=currently_tracking_markup)


def get_status(update, context):
    update.message.reply_text('Вот статус вашего заказа...', reply_markup=status_markup)


def get_help(update, context):
    update.message.reply_text('Чтобы получить статус вашей доставки напишите\n/status <номер заказа>',
                              reply_markup=help_markup)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('status', get_status))
    dp.add_handler(CommandHandler('help', get_help))
    dp.add_handler(CommandHandler('track', start_tracking))
    dp.add_handler(CommandHandler('stop_tracking', stop_tracking))
    dp.add_handler(CommandHandler('currently_tracking', currently_tracking))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
