from django.core.management import call_command
from django.core.management.base import BaseCommand

from portfolio.models import AboutMe, PortfolioCategory, PortfolioPhoto, SiteInfo


class Command(BaseCommand):
    help = "Load initial portfolio content from fixtures when the database is empty."

    def handle(self, *args, **options):
        has_content = any(
            [
                SiteInfo.objects.exists(),
                AboutMe.objects.exists(),
                PortfolioCategory.objects.exists(),
                PortfolioPhoto.objects.exists(),
            ]
        )

        if has_content:
            self.stdout.write(
                self.style.WARNING("Initial content skipped because database already has data.")
            )
            return

        call_command("loaddata", "initial_content", verbosity=0)
        self.stdout.write(self.style.SUCCESS("Initial content loaded."))
