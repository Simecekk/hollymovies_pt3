from django.core.management.base import BaseCommand
from hollymovies_app.models import CinemaScreening
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = "Deleting movie screenings older than 2 weeks"

    def handle(self, *args, **options):
        two_weeks_old_dt = timezone.now() - timedelta(days=14)
        cinema_screenings = CinemaScreening.objects.filter(screening_time__lte=two_weeks_old_dt)
        cinema_screenings.delete()
