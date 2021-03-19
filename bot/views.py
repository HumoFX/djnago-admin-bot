from django.conf import settings
from django.shortcuts import render
from django_telegrambot.apps import DjangoTelegramBot


def index(request):
    bot_list = DjangoTelegramBot.bots
    context = {'bot_list': bot_list, 'update_mode': settings.DJANGO_TELEGRAMBOT['MODE']}
    return render(request, 'bot/index.html', context)
