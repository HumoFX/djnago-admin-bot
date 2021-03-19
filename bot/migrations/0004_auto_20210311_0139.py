# Generated by Django 3.0.3 on 2021-03-11 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_telegramuser_university'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='language',
            field=models.CharField(choices=[('uz', "🇺🇿 O'zbekcha"), ('en', '🇺🇸 English'), ('ru', '🇷🇺 Русский')], default='uz', max_length=64),
        ),
    ]
