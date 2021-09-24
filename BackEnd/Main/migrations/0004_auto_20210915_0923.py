# Generated by Django 3.2.3 on 2021-09-15 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0003_alter_profile_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interestRate', models.FloatField(default=0.07)),
                ('bankAccountMoney', models.FloatField()),
                ('bankAccountMoney_IsValid', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanFundTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.IntegerField(choices=[(1, 'Loan Providers'), (2, 'Loan Customers'), (3, 'Bank Personnel'), (3, 'Bank Personnel')], default=2)),
                ('max', models.IntegerField()),
                ('min', models.IntegerField()),
                ('interestRate', models.FloatField()),
                ('bankPersonnel', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='LoanFundTerm', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='LoanTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.IntegerField(choices=[(1, 'Loan Providers'), (2, 'Loan Customers'), (3, 'Bank Personnel'), (3, 'Bank Personnel')], default=2)),
                ('interestRate', models.FloatField()),
                ('bankPersonnal', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='LoanTerm', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoansFunds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('Type', models.IntegerField(choices=[(1, 'Loan Providers'), (2, 'Loan Customers'), (3, 'Bank Personnel'), (3, 'Bank Personnel')], default=2)),
                ('interestRate', models.FloatField()),
                ('loanFundTerm', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Main.loanfundterm')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interestRate', models.FloatField()),
                ('amount', models.IntegerField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('bankPersonnel', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='loansApproved', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='loans', to=settings.AUTH_USER_MODEL)),
                ('loanTerm', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='loans', to='Main.loanterm')),
            ],
        ),
        migrations.CreateModel(
            name='Installments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dueDate', models.DateField()),
                ('amount', models.FloatField()),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='installments', to='Main.loan')),
            ],
        ),
    ]