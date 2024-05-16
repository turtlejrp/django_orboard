from django.core.management.base import BaseCommand
from dashboard.models import Cycletime
from datetime import date,time

class Command(BaseCommand):
    help = 'Insert data into the Cycletime model'

    def handle(self, *args, **kwargs):
        # Data to be inserted
        cycletime = [
            {'partno': '1234', 'create_at_time': time(8,15,00)},
            {'partno': '1234', 'create_at_time': time(8,16,00)},
            {'partno': '1234', 'create_at_time': time(8,17,00)},
        ]

        # Insert data into the Person model
        for cycletime_data in cycletime:
            cycletime, created = Cycletime.objects.get_or_create(**cycletime_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added {cycletime.partno} {cycletime.create_at_time}'))
            else:
                self.stdout.write(self.style.WARNING(f'{cycletime.partno} {cycletime.create_at_time} already exists'))

