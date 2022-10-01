from django.core.management import call_command


def update_db():
    call_command('updatedb')
