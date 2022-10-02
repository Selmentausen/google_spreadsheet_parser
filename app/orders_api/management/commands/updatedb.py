from django.core.management.base import BaseCommand

from orders_api.api_calls.google_sheets import get_sheet_data
from orders_api.api_calls.usd_to_rub_exchange_rate import get_usd_to_rub_exchange_rate
from orders_api.models import Order


class Command(BaseCommand):
    help = "Updates database with data from Google Sheets"

    def handle(self, *args, **options):
        spreadsheet_data = get_sheet_data()
        exchange_rate = get_usd_to_rub_exchange_rate()
        # Добавляем или обновляем данные с Google Sheets в нашу базу данных
        for item_id, values in spreadsheet_data.items():
            order, _ = Order.objects.update_or_create(
                id=item_id, defaults={**values, 'rub_cost': values['usd_cost'] * exchange_rate}
            )
            order.save()
        # Удаляем все что есть в нашей базе но нету в Google Sheets
        Order.objects.exclude(id__in=spreadsheet_data.keys()).delete()
        self.stdout.write(self.style.SUCCESS("Database successfully updated!"))
