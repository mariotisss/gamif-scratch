import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from teams.models import Team
from copilot_metrics.models import CopilotEngagementMetric

class Command(BaseCommand):
    help = "Import Copilot engagement metrics from a CSV-file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            type=str,
            help="Path to the CSV file",
        )

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        self.stdout.write(f"Importing Copilot metrics from {csv_path}...")

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                team_name = row["team"]
                date_str = row["date"]
                total_active = int(row["total_active_users"])
                total_engaged = int(row["total_engaged_users"])
                engagement_rate = float(row["engagement_rate"])

                # Crear u obtener el equipo
                team, created = Team.objects.get_or_create(name=team_name)

                # Convertir fecha
                date = datetime.strptime(date_str, "%Y-%m-%d").date()

                # Crear o actualizar métrica
                metric, created = CopilotEngagementMetric.objects.update_or_create(
                    team=team,
                    date=date,
                    defaults={
                        "total_active_users": total_active,
                        "total_engaged_users": total_engaged,
                        "engagement_rate": engagement_rate,
                    },
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Import finished. '{count}' rows processed."))
