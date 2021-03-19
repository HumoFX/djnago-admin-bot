import requests
from django.core.exceptions import ValidationError
from django.db import models

from edubookBot.local_settings import DJANGO_TELEGRAMBOT


class University(models.Model):
    name = models.CharField(max_length=512, verbose_name='Имя')
    name_ru = models.CharField(max_length=512, verbose_name='Имя(рус)', null=True, blank=True)
    name_en = models.CharField(max_length=512, verbose_name='Имя(анг)', null=True, blank=True)
    abbreviation = models.CharField(max_length=56, verbose_name='Аббревиатура', null=True, blank=True)
    abbreviation_ru = models.CharField(max_length=56, verbose_name='Аббревиатура', null=True, blank=True)
    abbreviation_en = models.CharField(max_length=56, verbose_name='Аббревиатура', null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=96)
    name_en = models.CharField(max_length=96, null=True)
    name_ru = models.CharField(max_length=96, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategory', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заглавие')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    file = models.FileField(upload_to='book/file/', null=True)
    file_id = models.CharField(max_length=256, verbose_name='Файл id в телеграм боте', null=True, blank=True)
    photo = models.ImageField(upload_to='book/img/', null=True)
    photo_id = models.CharField(max_length=256, verbose_name='Фото id в телеграм боте', null=True, blank=True)
    description = models.CharField(max_length=512, verbose_name='Описание', null=True, blank=True)
    author = models.CharField(max_length=512, verbose_name='Автор', null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)
    deep_link = models.CharField(max_length=256, verbose_name='Ссылка', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} \t\t {self.author}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        files = {'document': self.file.file}
        chat_id = 996288857
        token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']
        data = {'chat_id': chat_id}
        url = f'https://api.telegram.org/bot{token}/sendDocument'
        response = requests.post(url, data=data, files=files)
        print(f"1 -{response.status_code}")
        if response.status_code != 200:
            raise ValidationError('Проблемы с файлом')
        else:
            self.file_id = response.json()['result']['document']['file_id']
        photo = {'photo': self.photo}
        data = {'chat_id': chat_id}
        url = f'https://api.telegram.org/bot{token}/sendPhoto'
        response = requests.post(url, data=data, files=photo)
        print(f"2 - {response.status_code}")
        if response.status_code != 200:
            raise ValidationError('Проблемы с файлом')
        else:
            self.photo_id = response.json()['result']['photo'][0]['file_id']
        super(Product, self).save()
        self.deep_link = f"https://telegram.me/edubooksbot?start={self.id}"
        return super(Product, self).save()


class Order(models.Model):
    user = models.ForeignKey('bot.TelegramUser', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return '{}'.format(self.user.first_name)
