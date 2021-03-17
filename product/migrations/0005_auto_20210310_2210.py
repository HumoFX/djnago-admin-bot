# Generated by Django 3.0.3 on 2021-03-10 22:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20200225_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Имя')),
                ('name_ru', models.CharField(max_length=512, verbose_name='Имя(рус)')),
                ('name_en', models.CharField(max_length=512, verbose_name='Имя(анг)')),
                ('abbreviation', models.CharField(max_length=56, verbose_name='Аббревиатура')),
                ('abbreviation_ru', models.CharField(max_length=56, verbose_name='Аббревиатура')),
                ('abbreviation_en', models.CharField(max_length=56, verbose_name='Аббревиатура')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='available',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='author',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='product',
            name='file',
            field=models.FileField(null=True, upload_to='book/file/'),
        ),
        migrations.AddField(
            model_name='product',
            name='file_id',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Файл id в телеграм боте'),
        ),
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(null=True, upload_to='book/img/'),
        ),
        migrations.AddField(
            model_name='product',
            name='photo_id',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Фото id в телеграм боте'),
        ),
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default=1, max_length=256, verbose_name='Заглавие'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.University'),
        ),
    ]