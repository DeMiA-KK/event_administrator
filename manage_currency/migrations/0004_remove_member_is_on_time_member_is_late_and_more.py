# Generated by Django 4.0.4 on 2022-05-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_currency', '0003_alter_member_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='is_on_time',
        ),
        migrations.AddField(
            model_name='member',
            name='is_late',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
    ]
