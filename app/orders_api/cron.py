from django.core.management import call_command


def update_db():
    """Функция будет выполняться каждую минуту"""
    call_command('updatedb')
