# Generated by Django 3.2.3 on 2021-09-16 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0008_loansfunds_bankpersonnal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loansfunds',
            name='interestRate',
        ),
        migrations.AlterField(
            model_name='loansfunds',
            name='bankPersonnal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='loanFunds', to=settings.AUTH_USER_MODEL),
        ),
    ]
