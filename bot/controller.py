from django.db.models import Sum, F, Q

from bot import markups, constants
from bot.models import Command, Feedback
from product.models import Order, Product, Category


def command_logging(user, message_id, text, from_menu=None, current_menu=None, to_menu=None, offset=0,
                    category_id=None, update=False):
    if update:
        Command.objects.filter(message_id=message_id,
                               user=user).update(
                               text=text,
                               from_menu=from_menu,
                               current_menu=current_menu,
                               to_menu=to_menu,
                               offset=offset,
                               category_id=category_id)
    else:
        Command.objects.create(user=user,
                               message_id=message_id,
                               text=text,
                               from_menu=from_menu,
                               current_menu=current_menu,
                               to_menu=to_menu,
                               offset=offset,
                               category_id=category_id)


class Controller:
    def __init__(self, bot, update, user, cart=None, last_command=None):
        self.bot = bot
        self.update = update
        self.user = user
        self.cart = cart
        self.last_command = last_command

    def get_lang(self):
        if self.user.get_language_display() == markups.languages[1][0]:
            return 'en'
        elif self.user.get_language_display() == markups.languages[1][1]:
            return 'ru'
        else:
            return 'uz'

    def start(self):
        text = 'Welcome {}!\n'.format(
            self.user.first_name if self.user.first_name else 'User')
        self.bot.sendMessage(self.update.message.chat_id,
                             text=text,
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def start_deep_linking(self, deep_link):
        self.bot.sendPhoto(chat_id=self.user.telegram_id,
                           photo=str(Product.objects.get(id=deep_link).photo_id))
        self.bot.sendDocument(chat_id=self.user.telegram_id,
                              document=Product.objects.get(id=deep_link).file_id)
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def home_control(self):
        if self.update.message.text == constants.messages[self.get_lang()][constants.make_order_menu]:
            self.category_select()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.cart_menu]:
            self.cart_check()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.my_orders_menu]:
            self.order_history()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.language_menu]:
            self.language_select()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.feedback_menu]:
            self.feedback()

        # else:
        #     self.bot.sendMessage(self.update.message.chat_id, text='? in ?')

    def cart_check(self):
        if self.last_command.current_menu == constants.cart_menu:
            offset = self.last_command.offset
            search_arg = self.update.message.text
            query = Q(author__icontains=search_arg) | Q(title__icontains=search_arg)
            markup = markups.product_list(query, self.get_lang(), offset, constants.LIMIT)
            text = constants.messages[self.get_lang()][constants.search_res].format(markup['count'])
            products = markup['text']
            print(f"pr {products}")
            for product in products:
                text += f"\n {product[0]}"
            new_message = self.bot.sendMessage(chat_id=self.update.message.chat_id,
                                               text=text,
                                               reply_markup=markup['keyboard'])
            command_logging(user=self.user,
                            message_id=new_message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.cart_menu,
                            to_menu=constants.pieces)

        elif self.last_command.from_menu == constants.home:
            text = constants.messages[self.get_lang()][constants.search_text]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.back_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.cart_menu,
                            to_menu=constants.home)

    def order_history(self):
        orders_history = Order.objects.filter(user=self.user)
        if orders_history.count() == 0:
            text = constants.messages[self.get_lang()][constants.no_orders_yet_msg]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)
        else:
            order_str = 'История закачек \n'
            counter = 1
            for order in orders_history:
                order_str += '{}.| {}\n'.format(counter, order.product.title)
                counter += 1

            self.bot.sendMessage(self.update.message.chat_id,
                                 text=order_str)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

    def language_select(self):
        if self.last_command.to_menu == constants.language and \
                any(self.update.message.text in x for x in markups.languages):
            self.user.language = constants.LANG_DICT.get(self.update.message.text)
            self.user.save()
            text = constants.messages[self.get_lang()][constants.lang_select_msg]

            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.home_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

        elif self.last_command.from_menu == constants.home:
            self.bot.sendMessage(self.update.message.chat_id,
                                 text='Choose your language:',
                                 reply_markup=markups.languages_markup)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.language)

    def feedback(self):
        if self.last_command.current_menu == constants.feedback:
            Feedback.objects.create(user=self.user,
                                    text=self.update.message.text)
            text = constants.messages[self.get_lang()][constants.feedback_succeed_msg]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.home_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

        elif self.last_command.from_menu == constants.home:
            text = constants.messages[self.get_lang()][constants.feedback_send_msg]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.back_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.feedback,
                            to_menu=constants.home)

    def go_home(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.welcome_msg],
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def go_back(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text='Back',
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def category_select(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.choose_type_msg],
                             reply_markup=markups.categories_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.category,
                        to_menu=constants.product)

    def product_select(self):
        try:
            category = Category.objects.get(
                Q(name=self.update.message.text) |
                Q(name_en=self.update.message.text) |
                Q(name_ru=self.update.message.text)
            )
        except Product.DoesNotExist:
            category = None
            return self.bot.sendMessage(self.update.message.chat_id,
                                        text='Enter valid category',
                                        reply_markup=markups.categories_markup(self.get_lang()))
        offset = self.last_command.offset
        query = Q(category_id=category.id)
        markup = markups.product_list(query, self.get_lang(), offset, constants.LIMIT)
        text = constants.messages[self.get_lang()][constants.search_res].format(markup['count'])
        products = markup['text']
        for product in products:
            text += f"\n {product[0]}"
        new_message = self.bot.sendMessage(self.update.message.chat_id,
                                           text=text,
                                           reply_markup=markup['keyboard'])
        command_logging(user=self.user,
                        message_id=new_message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.category,
                        current_menu=constants.product,
                        to_menu=constants.pieces,
                        category_id=category.id)

    def pieces_select(self):
        if self.update.callback_query:
            query = self.update.callback_query
            query.answer()
            if Command.objects.filter(message_id=query.message.message_id, user=self.user).last() is not None:

                last_command = Command.objects.filter(message_id=query.message.message_id, user=self.user).last()
            else:
                last_command = self.last_command
            if query.data[:6] == "offset":
                offset = query.data[7:]
                query_filter = None
                #
                # if Command.objects.filter(message_id=query.message.message_id, user=self.user).last() is not None:
                #
                #     last_command = Command.objects.filter(message_id=query.message.message_id, user=self.user).last()
                # else:
                #     last_command = self.last_command
                category_id = last_command.category_id
                search_text = last_command.text
                if category_id:
                    query_filter = Q(category_id=category_id)
                elif last_command.current_menu == constants.cart_menu or category_id is None:
                    query_filter = Q(author__icontains=search_text) | Q(title__icontains=search_text)
                markup = markups.product_list(query_filter, self.get_lang(), int(offset), constants.LIMIT)
                text = constants.messages[self.get_lang()][constants.choose_book_msg]
                products = markup['text']
                for product in products:
                    text += f"\n {product[0]}"

                self.bot.editMessageText(chat_id=query.message.chat.id,
                                         message_id=query.message.message_id,
                                         text=text,
                                         reply_markup=markup['keyboard'])

                command_logging(user=self.user,
                                message_id=query.message.message_id,
                                text=search_text,
                                from_menu=last_command.current_menu,
                                current_menu=constants.pieces,
                                to_menu=last_command.current_menu,
                                offset=offset,
                                category_id=category_id,
                                update=True)
            else:
                product = Product.objects.get(id=query.data)
                self.bot.sendPhoto(chat_id=query.message.chat.id,
                                   photo=str(product.photo_id),
                                   caption=f"{product.title}\n {product.author}")
                self.bot.sendDocument(chat_id=query.message.chat.id,
                                      document=Product.objects.get(id=query.data).file_id)
                Order.objects.create(
                    user=self.user,
                    product=product
                )
                command_logging(user=self.user,
                                message_id=query.message.message_id,
                                text=query.data,
                                from_menu=last_command.current_menu,
                                current_menu=constants.pieces,
                                to_menu=last_command.current_menu,
                                update=True)
