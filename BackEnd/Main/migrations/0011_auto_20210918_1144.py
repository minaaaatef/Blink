# Generated by Django 3.2.3 on 2021-09-18 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_loanfundterm_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='bankAccountMoney_IsValid',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='interestRate',
        ),
        migrations.AddField(
            model_name='installments',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='loanterm',
            name='BankProfitRate',
            field=models.FloatField(default=0.01),
        ),
        migrations.AddField(
            model_name='loanterm',
            name='RiskRate',
            field=models.FloatField(default=0.02),
        ),
        migrations.AddField(
            model_name='loanterm',
            name='duration',
            field=models.IntegerField(default=12),
        ),
        migrations.CreateModel(
            name='FundsInstallments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dueDate', models.DateField()),
                ('amount', models.FloatField()),
                ('paid', models.BooleanField(default=False)),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installments', to='Main.loansfunds')),
            ],
        ),
    ]
