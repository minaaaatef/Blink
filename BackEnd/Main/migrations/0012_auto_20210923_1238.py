# Generated by Django 3.2.7 on 2021-09-23 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0011_auto_20210918_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='bankPersonnel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='loansApproved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loan',
            name='endDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanfundterm',
            name='Type',
            field=models.IntegerField(choices=[(1, 'Yearly'), (2, 'Monthly'), (3, 'Quarterly')], default=2),
        ),
        migrations.AlterField(
            model_name='loansfunds',
            name='endDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanterm',
            name='Type',
            field=models.IntegerField(choices=[(1, 'Yearly'), (2, 'Monthly'), (3, 'Quarterly')], default=2),
        ),
    ]
