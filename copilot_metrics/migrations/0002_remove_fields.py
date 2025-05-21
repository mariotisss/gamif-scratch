from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('copilot_metrics', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(name='UserTeam'),
        migrations.DeleteModel(name='Team'),
    ]
