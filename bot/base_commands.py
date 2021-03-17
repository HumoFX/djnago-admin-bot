import logging

from django.db.models import Q

from bot import constants, markups
from bot.models import Command, TelegramUser
from bot.constants import language
from product.models import University

logger = logging.getLogger(__name__)


def get_lang(user: TelegramUser):
    if user.get_language_display() == markups.languages[1][0]:
        return 'en'
    elif user.get_language_display() == markups.languages[1][1]:
        return 'ru'
    else:
        return 'uz'


def register(bot, user: TelegramUser, update):
    if update.message.text:

        university = University.objects.filter(
            Q(name=update.message.text) |
            Q(name_en=update.message.text) |
            Q(name_ru=update.message.text)
        )
        if university:
            user.university = university.first()
            user.is_registered = True
            user.save()
            Command.objects.create(user=user,
                                   message_id=update.message.message_id,
                                   text=constants.register,
                                   to_menu=constants.home)
            return bot.sendMessage(update.message.chat_id,
                                   text=constants.register_succeed_msg,
                                   reply_markup=markups.home_markup(get_lang(user)))
        else:
            bot.sendMessage(update.message.chat_id,
                            text=constants.ask_contact_msg,
                            reply_markup=markups.university_markup(get_lang(user)))
            Command.objects.create(user=user,
                                   message_id=update.message.message_id,
                                   text=update.message.text,
                                   to_menu=constants.home)
            return None

    if user.university is None:
        bot.sendMessage(update.message.chat_id,
                        text=constants.ask_contact_msg,
                        reply_markup=markups.university_markup(get_lang(user)))
        Command.objects.create(user=user,
                               message_id=update.message.message_id,
                               text=update.message.text,
                               to_menu=constants.home)
        return None


def help_me(bot, update):
    bot.sendMessage(update.message.chat_id, text='Call: 911')


def sticker(bot, update):
    bot.sendSticker(update.message.chat_id, sticker=update.message.sticker)


def error(bot, update, errors):
    logger.warning('Update "%s" caused error "%s"' % (update, errors))
