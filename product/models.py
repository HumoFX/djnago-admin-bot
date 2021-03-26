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
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='book/file/', null=True, blank=True)
    file_id = models.CharField(max_length=256, verbose_name='Файл id в телеграм боте', null=True, blank=True)
    photo = models.ImageField(upload_to='book/img/', null=True, blank=True)
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
