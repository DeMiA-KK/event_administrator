# Generated by Django 4.0.4 on 2022-05-20 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_currency', '0013_alter_answer_quiz_alter_quiz_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finishedquiz',
            name='quizes',
        ),
        migrations.AddField(
            model_name='finishedquiz',
            name='quiz',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='finished_quize', to='manage_currency.quiz'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='finishedquiz',
            name='selected_choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_choice', to='manage_currency.quizoption'),
        ),
        migrations.AlterField(
            model_name='finishedquiz',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_currency.team'),
        ),
    ]