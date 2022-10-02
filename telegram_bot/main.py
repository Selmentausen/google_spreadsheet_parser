import os
import logging

import psycopg2
from telegram.ext import Updater, CommandHandler
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", '5655136236:AAHeKyqqIcolMiHGtp0mrsiJZq8wdeup-TY')
conn = psycopg2.connect(
    database=os.environ.get('SQL_DATABASE', 'test_case_db'),
    user=os.environ.get('SQL_USER', 'admin'), password=os.environ.get('SQL_PASSWORD', 'admin123'),
    host=os.environ.get('SQL_HOST', '127.0.0.1'), port=os.environ.get('SQL_PORT', '5432'))
cursor = conn.cursor()


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def get_order_from_db(order_id):
    cursor.execute(f"SELECT * FROM orders_api_order WHERE order_id='{order_id}'")
    order = cursor.fetchone()  # requests.get(api_url).json()
    if order:
        return order
    return None


def remind_delivery(context):
    job = context.job
    cursor.execute(
        f"""DELETE FROM telegram_bot_trackingorders 
WHERE user_id={job.context['user_id']} AND order_id='{job.context['order_id']}'"""
    )
    conn.commit()
    context.bot.send_message(job.context['chat_id'],
                             text=f'Наступил срок доставки заказа {job.context["order_id"]}')


def start_tracking(update, context):
    order_id = context.args[0] if context.args else context.user_data.get('order_id', None)
    if not order_id:
        update.message.reply_text(f'Пожалуйста введите номер заказа\n/track <номер заказа>')
        return

    order = get_order_from_db(order_id)
    if not order:
        update.message.reply_text(f'Мы не нашли заказ с номером {order_id}')
        return

    user_id = update.message.from_user['id']
    cursor.execute(
        f"SELECT * FROM telegram_bot_trackingorders WHERE user_id={user_id} AND order_id='{order_id}'")
    if cursor.fetchall():
        update.message.reply_text(f'Вы уже отслеживаете заказ {order_id}')
        return
    cursor.execute(f"INSERT INTO telegram_bot_trackingorders (user_id, order_id) VALUES ({user_id}, '{order_id}')")
    reminder_time = datetime.datetime.combine(order[-1], datetime.time(9, 0, 0))
    chat_id = update.message.chat_id
    job_context = {'chat_id': chat_id, 'user_id': user_id, 'order_id': order_id}
    context.job_queue.run_once(remind_delivery, reminder_time, name=str(chat_id), context=job_context)
    conn.commit()
    update.message.reply_text(f'Мы вас уведомим когда наступит дата заказа {order_id}')


def stop_tracking(update, context):
    order_id = context.args[0] if context.args else context.user_data.get('order_id', None)
    if not order_id:
        update.message.reply_text(f'Пожалуйста введите номер заказа\n/stop_tracking <номер заказа>')
        return
    order = get_order_from_db(order_id)
    if not order:
        update.message.reply_text(f'Мы не нашли заказ с номер {order_id}')
        return
    user_id = update.message.from_user['id']
    cursor.execute(
        f"DELETE FROM telegram_bot_trackingorders WHERE user_id={user_id} AND order_id='{order_id}'")
    conn.commit()
    update.message.reply_text(f'Вы прекратили отслеживать заказ {order_id}')


def currently_tracking(update, context):
    user_id = update.message.from_user['id']
    cursor.execute(f'SELECT order_id FROM telegram_bot_trackingorders WHERE user_id={user_id}')
    order_list = '\n- '.join([item[0] for item in cursor.fetchall()])
    if not order_list:
        update.message.reply_text('Вы пока не отслеживаете заказы')
        return
    update.message.reply_text(f'Вот все заказы которые вы отслеживаете\n{order_list}')


def get_status(update, context):
    try:
        order_id = context.args[0]
    except IndexError:
        update.message.reply_text(f'Пожалуйста введите номер заказа\n/status <номер заказа>')
        return
    order = get_order_from_db(order_id)
    if order:
        delivery_date = order[-1].strftime("%d.%m.%Y")
        context.user_data['order_id'] = order_id
        update.message.reply_text(f'Заказ {order_id} будет доставлен {delivery_date}')
    else:
        update.message.reply_text(f'Мы не нашли заказ с номером {order_id}')


def get_help(update, context):
    update.message.reply_text(
        """Доступные команды
- /status <номер заказа>
- /track <номер заказа>
- /stop_tracking <номер заказа>
- /currently_tracking"""
    )


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    track = CommandHandler('track', start_tracking)
    status = CommandHandler('status', get_status)

    dp.add_handler(CommandHandler('help', get_help))
    dp.add_handler(status)
    dp.add_handler(track)
    dp.add_handler(CommandHandler('stop_tracking', stop_tracking))
    dp.add_handler(CommandHandler('currently_tracking', currently_tracking))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
