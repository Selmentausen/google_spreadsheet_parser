from django.core.management.base import BaseCommand


from orders.api_calls.google_spreadsheet import get_spreadsheet_data
from orders.api_calls.usd_to_rub_exchange_rate import get_usd_to_rub_exchange_rate
from orders.models import Orders


class Command(BaseCommand):
    help = "Updates database with data from Google spreadsheet"

    def handle(self, *args, **options):
        spreadsheet_data = get_spreadsheet_data()
        exchange_rate = get_usd_to_rub_exchange_rate()
        for item_id, values in spreadsheet_data.items():
            order, _ = Orders.objects.update_or_create(id=item_id,
                                                       defaults={**values,
                                                                 'rub_cost': values['usd_cost'] * exchange_rate})
            order.save()
        Orders.objects.exclude(id__in=spreadsheet_data.keys()).delete()
        self.stdout.write(self.style.SUCCESS("Database successfully updated!"))
