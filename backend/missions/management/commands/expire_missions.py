from django.core.management.base import BaseCommand
from missions.models import Mission
from datetime import datetime

class Command(BaseCommand):
    help = 'Desactiva automáticamente las misiones que hayan expirado'

    def handle(self, *args, **kwargs):
        now = datetime.now()
        expired = Mission.objects.filter(
            is_active=True,
            time_limit_days__isnull=False  # Condición de filtro en una query Django ORM
        )

        count = 0
        for mission in expired:
            exp = mission.expiration_date()
            if exp and exp < now:
                mission.is_active = False
                mission.save()
                count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {count} misiones expiradas desactivadas"))
