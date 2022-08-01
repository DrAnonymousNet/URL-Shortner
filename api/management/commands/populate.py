from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from api.models import Link


class Command(BaseCommand):
    help = "Populates the database with the data above"

    def handle(self, *args, **options):
        try:

            for i in range(7, 30000):
                long_link = f"https://www.nairaland.com/{i}"
                new_link = Link.objects.create(long_link=long_link, owner_id=1)
                self.stdout.write(self.style.SUCCESS(
                    f"link {new_link} added successfully"))

        except Exception as e:
            raise CommandError(f"{e}")
        self.stdout.write(self.style.SUCCESS(
            "All links data added successfull !"))
