from django_telegrambot.apps import DjangoTelegramBot, logger
from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, CallbackContext

from bot import constants
from bot.base_commands import register, sticker
from bot.controller import Controller
from bot.models import TelegramUser, Command


def error(update: Update, context: CallbackContext, error):
    if error.message == "Message is not modified":
        # print your string
        return
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def file_upload(update: Update, context: CallbackContext):
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=update.message.chat.id)
    print(user)
    if created:
        user.first_name = update.message.chat.first_name
        user.last_name = update.message.chat.last_name
        user.username = update.message.chat.username
        user.save()
    file = context.bot.get_file(update.message.document)
    print(file)
    try:
        last_command = Command.objects.filter(user=user).last()
    except Command.DoesNotExist:
        last_command = None
    print(last_command)
    Controller(context.bot, update, user, last_command).add_book(product=file)


def photo_upload(update: Update, context: CallbackContext):
    pass


def bot_inline_control(update: Update, context: CallbackContext):
    query = update.callback_query
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=query.message.chat.id)
    if created:
        user.first_name = query.message.chat.first_name
        user.last_name = query.message.chat.last_name
        user.username = query.message.chat.username
        user.save()

    try:
        cart = user.cart.all()
    except:
        cart = None
    if not user.is_registered:
        return register(context.bot, user, update)
    try:
        last_command = Command.objects.filter(user=user).last()
    except Command.DoesNotExist:
        last_command = None

    if update.callback_query:
        Controller(context.bot, update, user, cart, last_command).pieces_select()


def bot_control(update: Update, context: CallbackContext):
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=update.message.chat_id)
    if created:
        user.first_name = update.message.from_user.first_name
        user.last_name = update.message.from_user.last_name
        user.username = update.message.from_user.username
        user.save()

    try:
        cart = user.cart.all()
    except:
        cart = None
    if not user.is_registered:
        return register(context.bot, user, update)
    if update.message.text == '/start':
        Controller(context.bot, update, user).start()
    if update.message.text.__contains__('/start') and len(update.message.text) > constants.deep_linking:
        deep_link = update.message.text[constants.deep_linking:]
        Controller(context.bot, update, user).start_deep_linking(deep_link)

    try:
        last_command = Command.objects.filter(user=user).last()
    except Command.DoesNotExist:
        last_command = None

    if update.message.text == 'Home':
        Controller(context.bot, update, user).go_home()

    elif update.message.text == 'ADD BOOK':
        Controller(context.bot, update, user, cart, last_command).add_book()

    elif update.message.text in ["🔙 Orqaga", '🔙 Back', "🔙 Назад", "orqaga", 'back', "назад"]:
        Controller(context.bot, update, user).go_home()

    elif last_command.to_menu == constants.language:
        Controller(context.bot, update, user, cart, last_command).language_select()

    elif last_command.to_menu == constants.category:
        Controller(context.bot, update, user, cart, last_command).category_select()

    elif last_command.to_menu == constants.product:
        Controller(context.bot, update, user, cart, last_command).product_select()

    elif last_command.current_menu == constants.add_book:
        Controller(context.bot, update, user, cart, last_command).add_book()

    elif last_command.current_menu == constants.product:
        Controller(context.bot, update, user, cart, last_command).product_select()

    elif last_command.current_menu == constants.feedback:
        Controller(context.bot, update, user, cart, last_command).feedback()

    elif last_command.current_menu == constants.cart_menu:
        Controller(context.bot, update, user, cart, last_command).cart_check()

    elif last_command.to_menu == constants.home:
        Controller(context.bot, update, user, cart, last_command).home_control()

    else:
        context.bot.sendMessage(update.message.chat_id, text='???')


def main():
    # updater = DjangoTelegramBot.updater

    dp = DjangoTelegramBot.dispatcher
    dp.add_handler(MessageHandler(Filters.text, bot_control))
    dp.add_handler(CallbackQueryHandler(bot_inline_control))
    dp.add_handler(MessageHandler(Filters.sticker, sticker))
    dp.add_handler(MessageHandler(Filters.document, file_upload))
    dp.add_handler(MessageHandler(Filters.photo, photo_upload))

    # updater.start_polling()
    # updater.idle()
    # updater.idle()
