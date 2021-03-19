from bot.models import TelegramUser
from product.models import Product, Order

user = TelegramUser.objects.last()
product = Product.objects.last()
