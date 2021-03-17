from django.db.models import Q
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot import constants
from product.models import Category, Product, University


def back_markup(lang):
    return ReplyKeyboardMarkup([
        [constants.messages[lang][constants.back_menu]]
    ])


def finish_order_markup(lang):
    return ReplyKeyboardMarkup([
        [constants.messages[lang][constants.finish_order_menu]],
        [constants.messages[lang][constants.back_menu]]
    ])


def university_markup(lang):
    if lang == 'en':
        universities = list(University.objects.all().values_list('name_en', flat=True))
    elif lang == 'ru':
        universities = list(University.objects.all().values_list('name_ru', flat=True))
    else:
        universities = list(University.objects.all().values_list('name', flat=True))
    universities.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup([universities])


def home_markup(lang):
    home = [
        [constants.messages[lang][constants.make_order_menu]],
        [constants.messages[lang][constants.cart_menu],
         constants.messages[lang][constants.my_orders_menu]],
        [constants.messages[lang][constants.language_menu],
         constants.messages[lang][constants.feedback_menu]]
    ]
    return ReplyKeyboardMarkup(home)


languages = [
    ["🇺🇿 O'zbekcha"],
    ['🇺🇸 English',
     '🇷🇺 Русский']
]
languages_markup = ReplyKeyboardMarkup(languages)


def categories_markup(lang):
    print(lang)
    if lang == 'en':
        categories = list(Category.objects.all().values_list('name_en', flat=True))
        print(categories)
    elif lang == 'ru':
        categories = list(Category.objects.all().values_list('name_ru', flat=True))
    else:
        categories = list(Category.objects.all().values_list('name', flat=True))
    categories.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup([categories[i:i + 2] for i in range(0, len(categories), 2)])


def product_list(query, lang, offset, limit):
    count = Product.objects.filter(query).count()
    print(f"count {count}")
    print(f"off {offset}")
    products = list(Product.objects.filter(query)[offset:offset + limit].values_list('title', 'id'))
    keyboard = []
    button = offset + 1
    for product in products:
        keyboard.append(InlineKeyboardButton(button, callback_data=f'{product[1]}'))
        button += 1
    if offset > 0:
        keyboard.append(InlineKeyboardButton("left", callback_data=f"offset:{offset - limit}"))
    if count > offset + limit:
        keyboard.append(InlineKeyboardButton("right", callback_data=f"offset:{offset + limit}"))

    return {'text': products, 'keyboard': InlineKeyboardMarkup([keyboard[i:i + 5] for i in range(0, len(keyboard), 5)])}


pieces = [str(x) for x in (range(1, 10))]


def pieces_markup(lang):
    pieces.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup(
        [pieces[i:i + 3] for i in range(0, len(pieces), 3)])
