# Generated by Django 4.0.4 on 2022-05-19 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_currency', '0012_finishedquiz_selected_choice_alter_quiz_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='quiz',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_of_answer', to='manage_currency.quiz'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='answer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_of_quiz', to='manage_currency.answer'),
        ),
    ]
