import sqlite3
from telebot.async_telebot import AsyncTeleBot
from telegram_keyboards import markup_for_inline_keyboard, markup_for_subscribe, markup_for_main_keyboard, markup_for_buy_keyboard, markup_for_balance, keybord_for_assets, keyboard_for_transaction_history, keyboard_for_back_to_profile, keyboard_for_course, markup_for_stats, keyboard_for_invoices
from asyncio import run
from telebot import types
from url import start_message_pic, buying_picture
from aiosend import CryptoPay
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fragment_requests import Fragment
from Apay import Apay

bot = AsyncTeleBot('токен бота')
cb = CryptoPay(token='токен CryptoBot')
fragment_token = "Fragment токен"
paymaster_token = "токен Apay"


USER_STATES = {
    'DEFAULT_STATE': 'default_state',
    'AWAITING_STARS_AMOUNT': 'awaiting_stars',
    'AWAITING_PAYMENT_CONFIRMATION': 'awaiting_payment',
    'AWAITING_SUPPORT': 'awaiting_support',
    'AWAITING_PROMO': 'waiting_promo',
    'AWAITING_ASSET': 'waiting_for_asset'
}

ADMIN_STATES = {
    "AWAITING_FOR_MAIL": "mail",
    "AWAITING_STATS": "stats",
    "AWAITING_CREATING_PROMO": "create_promo",
    "AWAITING_USDT_COURSE": "usdt_change",
    "AWAITING_TON_COURSE": "ton_change",
    "AWAITING_STAR_COURSE": "star_change",
    "AWAITING_FOR_NEW_ADMIN": "new_admin",
    "AWAITING_FOR_DELETE_ADMIN": "delete_admin"
}


SUPPORT_CHAT_ID = '-1002549120267'

con = sqlite3.connect('StarBotClient.db')
cur = con.cursor()


# обработчик команды /start
@bot.message_handler(commands=['start'])
async def start(message: types.Message):
    cur.execute('SELECT 1 FROM Clients WHERE user_id = ?', (message.from_user.id,))

    if cur.fetchone():
        cur.execute('''
            UPDATE Clients 
            SET state = ?,
                amount = ?,
                chat_id = ? 
            WHERE user_id = ?
        ''', (USER_STATES["DEFAULT_STATE"], 0, message.chat.id, message.from_user.id))
    else:
        cur.execute('''
            INSERT INTO Clients (user_id, state, amount, chat_id) 
            VALUES (?, ?, ?, ?)
        ''', (message.from_user.id, USER_STATES["DEFAULT_STATE"], 0, message.chat.id))

    con.commit()

    markup_subscribe = markup_for_subscribe
    await bot.send_message(message.chat.id, '<b>Приветствую в NestxStar🛒. Данный бот специализируется на автоматической продаже звезд✨.\n\n📈Здесь ты можешь приобрести звезды по низкому курсу, без задержек и риска.\n\n‼️Чтобы приступить к покупке звезд, пожалуйста, подпишись на канал ниже</b>', parse_mode="HTML", reply_markup=markup_subscribe)


# обработчик каллбэка на проверку подписки
@bot.callback_query_handler(func=lambda callback: callback.data == 'success_subscribe')
async def check_subscribe(callback: types.CallbackQuery):
    try:
        is_member = await bot.get_chat_member('-1002709568442', user_id=callback.from_user.id)

        if is_member.status in ['member', 'administrator', 'creator']:
            await bot.answer_callback_query(callback_query_id=callback.id, text='✅Вы успешно прошли проверку')
            await bot.delete_message(callback.message.chat.id, callback.message.id)
            await bot.send_photo(callback.message.chat.id, start_message_pic, reply_markup=markup_for_inline_keyboard)

        else:
            await bot.answer_callback_query(callback_query_id=callback.id, text='❌Вы не подписаны на канал!')

    except Exception as e:
        await bot.send_message(callback.message.chat.id, "❌Произошла ошибка, пожалуйста попробуйте снова.")


@bot.callback_query_handler(func=lambda call: call.data == "buy_stars")
async def buy_stars(call: types.CallbackQuery):
    try:

        cur.execute(f'''UPDATE Clients
                        SET state = "{USER_STATES["AWAITING_STARS_AMOUNT"]}"
                        WHERE user_id = "{call.from_user.id}"
        ''')
        await bot.answer_callback_query(call.id)
        con.commit()
        await bot.send_message(call.message.chat.id, 'Пожалуйста, введите ниже количество звезд, которое вы хотите приобрести\n\n<b>Минимальное количество - 50 звезд🌟</b>', parse_mode="HTML")

    except Exception as e:
        await bot.send_message(call.message.chat.id, 'Произошла ошибка, пожалуйста, попробуйте позже еще раз.')


@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = {str(message.from_user.id)}').fetchone()[0] == USER_STATES["AWAITING_STARS_AMOUNT"] and message.text != '/cancel')
async def get_amount(message: types.Message):
    try:
        stars_amount = int(message.text)
        if stars_amount >= 50:
            cur.execute(f'''UPDATE Clients  
                            SET amount = {stars_amount}
                            WHERE user_id = {message.from_user.id}
                        ''')
            cur.execute(f'''UPDATE Clients
                            SET state = "{USER_STATES["DEFAULT_STATE"]}"
                            WHERE user_id = "{message.from_user.id}"
                            ''')
            con.commit()
            star_course = cur.execute('SELECT STAR_COURSE FROM Exchange_rate').fetchone()[0]
            await bot.send_photo(message.chat.id, photo=buying_picture, caption=f'<b><i>🌟Количество звезд:</i></b> <code>{message.text} звезд</code>\n<b><i>👥Юзернэйм:</i></b> <code>{message.from_user.username}</code>\n<b><i>💸Сумма к оплате:</i></b> <code>{int(int(message.text) * float(star_course))}руб.</code>', reply_markup=markup_for_buy_keyboard, parse_mode="HTML")

        else:
            await bot.send_message(message.chat.id, '<b>Минимальное количество звезд - 50⭐, пожалуйста, попробуйте снова</b>', parse_mode="HTML")
            cur.execute('''
                        UPDATE Clients 
                        SET state = ?,
                            amount = ?
                        WHERE user_id = ?
                    ''', (USER_STATES["DEFAULT_STATE"], 0, message.from_user.id))
            con.commit()

    except ValueError:
        await bot.send_message(message.chat.id, '<i><b>❌Пожалуйста, введите корректное количество звезд</b></i>', parse_mode="HTML")
        cur.execute('''
                    UPDATE Clients 
                    SET state = ?,
                        amount = ?
                    WHERE user_id = ?
                ''', (USER_STATES["DEFAULT_STATE"], 0, message.from_user.id))
        con.commit()

    except Exception as e:
        await bot.send_message(message.chat.id, f'Произошла ошибка, попробуйте снова. {e}')
        cur.execute('''
                    UPDATE Clients 
                    SET state = ?,
                        amount = ?
                    WHERE user_id = ?
                ''', (USER_STATES["DEFAULT_STATE"], 0, message.from_user.id))
        con.commit()

@bot.callback_query_handler(func=lambda call: call.data == 'buy_approve')
async def buy_approve(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(call.message.chat.id, text='<b>Выберите способ оплаты ниже:</b>', reply_markup=keybord_for_assets, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data in ['USDT', 'TON', 'RUB'])
async def get_asset_and_invoice(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    try:
        ton, usdt, star_course = cur.execute(f'SELECT TON, USDT, STAR_COURSE FROM Exchange_rate').fetchone()
        amount = int(cur.execute(f'''SELECT amount FROM Clients WHERE user_id = {call.from_user.id}''').fetchone()[0])
        if call.data == 'USDT':
            total_sum = (amount * star_course / usdt)
            if not cur.execute(f'SELECT * FROM Invoices WHERE user_id = {call.from_user.id}').fetchall():
                invoice = await cb.create_invoice(amount=total_sum, asset="USDT", description=f'Оплата {amount} звезд',
                                                  paid_btn_name=f'openBot', allow_comments=False, allow_anonymous=False,
                                                  paid_btn_url='https://t.me/Startelebot')
                cur.execute(f'''INSERT INTO Invoices(invoice_id, user_id, status, sum) VALUES("{invoice.invoice_id}", {call.from_user.id}, "{invoice.status}", {amount})''')
                con.commit()
                keyboard = InlineKeyboardMarkup()
                kb = InlineKeyboardButton('🛒Оплатить', url=invoice.bot_invoice_url)
                kb2 = InlineKeyboardButton('✅Готово', callback_data='try_to_buy')
                keyboard.row(kb)
                keyboard.row(kb2)

            else:
                cur.execute(f'DELETE FROM Invoices WHERE user_id = {call.from_user.id}')
                con.commit()
                amount = int(cur.execute(f'''SELECT amount FROM Clients WHERE user_id = {call.from_user.id}''').fetchone()[0])
                invoice = await cb.create_invoice(amount=total_sum, asset="USDT", description=f'Оплата {amount} звезд',
                                                  paid_btn_name=f'openBot', allow_comments=False, allow_anonymous=False,
                                                  paid_btn_url='https://t.me/Startelebot')
                cur.execute(
                    f'''INSERT INTO Invoices(invoice_id, user_id, status, sum) VALUES("{invoice.invoice_id}", {call.from_user.id}, "{invoice.status}", {amount})''')
                con.commit()
                keyboard = InlineKeyboardMarkup()
                kb = InlineKeyboardButton('🛒Оплатить', url=invoice.bot_invoice_url)
                kb2 = InlineKeyboardButton('✅Готово', callback_data='try_to_buy')
                keyboard.row(kb)
                keyboard.row(kb2)

                cur.execute(f'''UPDATE Clients
                                SET state = "{USER_STATES["DEFAULT_STATE"]}"
                                WHERE user_id = "{call.message.from_user.id}"
                                ''')
                con.commit()

        elif call.data == 'TON':
            total_sum = (amount * star_course) / ton
            if not cur.execute(f'SELECT * FROM Invoices WHERE user_id = {call.from_user.id}').fetchall():
                invoice = await cb.create_invoice(amount=total_sum, asset="TON", description=f'Оплата {amount} звезд',
                                                  paid_btn_name=f'openBot', allow_comments=False, allow_anonymous=False,
                                                  paid_btn_url='https://t.me/Startelebot')
                cur.execute(
                    f'''INSERT INTO Invoices(invoice_id, user_id, status, sum) VALUES("{invoice.invoice_id}", {call.from_user.id}, "{invoice.status}", {amount})''')
                con.commit()
                keyboard = InlineKeyboardMarkup()
                kb = InlineKeyboardButton('🛒Оплатить', url=invoice.bot_invoice_url)
                kb2 = InlineKeyboardButton('✅Готово', callback_data='try_to_buy')
                keyboard.row(kb)
                keyboard.row(kb2)

            else:
                cur.execute(f'DELETE FROM Invoices WHERE user_id = {call.from_user.id}')
                con.commit()
                amount = int(cur.execute(f'''SELECT amount FROM Clients WHERE user_id = {call.from_user.id}''').fetchone()[0])
                invoice = await cb.create_invoice(amount=total_sum, asset="TON", description=f'Оплата {amount} звезд',
                                                  paid_btn_name=f'openBot', allow_comments=False, allow_anonymous=False,
                                                  paid_btn_url='https://t.me/Startelebot')
                cur.execute(
                    f'''INSERT INTO Invoices(invoice_id, user_id, status, sum) VALUES("{invoice.invoice_id}", {call.from_user.id}, "{invoice.status}", {amount})''')
                con.commit()
                keyboard = InlineKeyboardMarkup()
                kb = InlineKeyboardButton('🛒Оплатить', url=invoice.bot_invoice_url)
                kb2 = InlineKeyboardButton('✅Готово', callback_data='try_to_buy')
                keyboard.row(kb)
                keyboard.row(kb2)

                cur.execute(f'''UPDATE Clients
                                SET state = "{USER_STATES["DEFAULT_STATE"]}"
                                WHERE user_id = "{call.message.from_user.id}"
                                ''')
                con.commit()

        elif call.data == 'RUB':
            total_sum = amount * star_course
            sum_for_amount = int(total_sum * 100)
            orders = cur.execute('SELECT user_id FROM Purchases').fetchone()

            if orders:
                order_id = f'order_{len(orders) + 1}'
            else:
                order_id = 'order_oacaqkk'

            is_orders = cur.execute(f'SElECT invoice_id FROM Invoices WHERE user_id = {call.from_user.id}').fetchone()
            if is_orders:
                await bot.send_message(call.message.chat.id, '<b>У вас уже есть открытые заказы!</b>', reply_markup=keyboard_for_invoices, parse_mode='HTML')

            else:
                cur.execute(f'INSERT INTO Invoices(invoice_id, user_id, status, sum) VALUES("{order_id}", {call.from_user.id}, "active", {total_sum})')
                con.commit()
                response = Apay.get_link(amount=sum_for_amount, id_order=order_id)
                keyboard = InlineKeyboardMarkup()
                kb = InlineKeyboardButton('🛒Оплатить', url=response['url'])
                kb2 = InlineKeyboardButton('✅Готово', callback_data='try_to_buy')
                keyboard.row(kb)
                keyboard.row(kb2)

                await bot.delete_message(call.message.chat.id, call.message.id)
                await bot.send_photo(call.message.chat.id, buying_picture, caption=f'<b>Количество звезд:</b> <code>{amount}</code>\n<b>Сумма к оплате:</b> <code>{total_sum} {call.data}</code>\n<i>После оплаты нажмите кнопку "Готово"</i>', reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        await bot.send_message(call.message.chat.id ,f'Ошибка: {e}')

@bot.callback_query_handler(func=lambda call: call.data == 'try_to_buy')
async def try_to_buy(call: types.CallbackQuery):
    order_id = cur.execute(f'SELECT invoice_id FROM Invoices WHERE user_id = {call.from_user.id}').fetchone()[0]
    is_success = Apay.check_payment(id_order=order_id)
    print(is_success)
    await bot.send_message(call.message.chat.id, is_success)

@bot.callback_query_handler(func=lambda call: call.data == 'close_invoices')
async def close_invoices(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    cur.execute(f'DELETE FROM Invoices WHERE user_id = {call.from_user.id}')
    con.commit()
    await bot.send_message(call.message.chat.id, '<b>Предыдущие заказы были удалены!\n\n❗ВАЖНО: предыдущие заказы больше не действительны. Если Вы их оплатите, то звезды не будут отправлены!</b>', parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'buy_cancel')
async def buy_cancel(call: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES['DEFAULT_STATE']}",
                        amount = 0
                    WHERE user_id = "{call.from_user.id}"''')
    con.commit()
    await bot.send_message(call.message.chat.id, '<i><b>🛍️Вы успешно отменили покупку, будем рады видеть вас снова!</b></i>', parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'promo')
async def promo(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, 'Вы выбрали раздел "Промокод"')
    await bot.send_message(call.message.chat.id, '<b><i>Приветствую. В данном разделе вы можете ввести промокод и получить звезды на Ваш баланс бесплатно!</i></b>\n\n<tg-spoiler>Все промокоды публикуются только в новостном канале!</tg-spoiler>', parse_mode="HTML")
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES["AWAITING_PROMO"]}"
                    WHERE user_id = "{call.from_user.id}"   
                    ''')
    con.commit()


@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = {str(message.from_user.id)}').fetchone()[0] == USER_STATES["AWAITING_PROMO"] and message.text != '/cancel')
async def check_promo(message: types.Message):
    try:
        bd_promo = cur.execute(f'SELECT * FROM Promo').fetchall()
        promocodes = [p[0] for p in bd_promo]

        if not promocodes:
            await bot.send_message(message.chat.id, '❌На данный момент нет активных промокодов. Все промокоды публикуются в новостном канале!', parse_mode="HTML")
            cur.execute(f'''UPDATE Clients
                            SET state = "{USER_STATES["DEFAULT_STATE"]}"
                            WHERE user_id = "{message.from_user.id}"
                            ''')
            con.commit()
            return

        elif message.text not in promocodes:
            await bot.send_message(message.chat.id, '<b>❌Данного промокода не существует, проверьте правильность написания</b>', parse_mode="HTML")
            cur.execute(f'''UPDATE Clients
                            SET state = "{USER_STATES["DEFAULT_STATE"]}"
                            WHERE user_id = "{message.from_user.id}"
                            ''')
            return

        used_promo = [p[0] for p in cur.execute(f'SELECT promo FROM used_promo WHERE user_id = {message.from_user.id}').fetchall()]

        if message.text in used_promo:
            await bot.send_message(message.chat.id, '<b>❌Вы уже использовали данный промокод ранее</b>', parse_mode="HTML")
            cur.execute(f'''UPDATE Clients
                            SET state = "{USER_STATES["DEFAULT_STATE"]}"
                            WHERE user_id = "{message.from_user.id}"
                            ''')
            return

        else:
            current_promo = cur.execute(f'SELECT * FROM Promo WHERE promo = "{message.text}"').fetchone()
            amount = current_promo[1]
            max_uses = current_promo[2]
            uses_now = current_promo[3]
            balance = cur.execute(f'SELECT balance FROM Clients WHERE user_id = "{message.from_user.id}"').fetchone()[0]

            if int(uses_now) >= int(max_uses):
                await bot.send_message(message.chat.id, '<b>❌Превышено количество использований данного промокода!</b>', parse_mode="HTML")

                cur.execute(f'''UPDATE Clients
                                SET state = "{USER_STATES["DEFAULT_STATE"]}"
                                WHERE user_id = "{message.from_user.id}"
                                ''')
                con.commit()
                return

            else:
                await bot.send_message(message.chat.id, f'<b><i>✔️Успех! Вы успешно активировали промокод и получили {amount} звезд на ваш баланс</i></b>\n<tg-spoiler>Для проверки баланса используй команду /profile</tg-spoiler>', parse_mode="HTML")

                cur.execute(f'''UPDATE Clients
                                SET balance = {balance + int(amount)}
                                WHERE user_id = "{message.from_user.id}"
                                ''')

                cur.execute(f'''UPDATE Promo
                                SET uses_now = {int(uses_now) + 1}
                                WHERE promo = "{message.text}"
                                ''')
                cur.execute(f'INSERT INTO used_promo(user_id, promo) VALUES({message.from_user.id}, "{message.text}")')

                cur.execute(f'''UPDATE Clients
                                SET state = "{USER_STATES["DEFAULT_STATE"]}"
                                WHERE user_id = "{message.from_user.id}"
                                ''')
                con.commit()

    except Exception as e:
        await bot.send_message(message.chat.id, 'Произошла ошибка, пожалуйста, попробуйте позже')

        cur.execute(f'''UPDATE Clients
                        SET state = "{USER_STATES["DEFAULT_STATE"]}"
                        WHERE user_id = "{message.from_user.id}"
                        ''')
        con.commit()


@bot.message_handler(commands=['promo'])
async def promocode(message: types.Message):
    await bot.send_message(message.chat.id, '<b><i>Приветствую. В данном разделе вы можете ввести промокод и получить звезды на Ваш баланс бесплатно!</i></b>\n\n<tg-spoiler>Все промокоды публикуются только в новостном канале!</tg-spoiler>', parse_mode="HTML")
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES["AWAITING_PROMO"]}"
                    WHERE user_id = "{message.from_user.id}"   
                    ''')
    con.commit()

@bot.message_handler(commands=['buy'])
async def buy_stars_command(message: types.Message):
    try:
        cur.execute(f'''UPDATE Clients
                        SET state = "{USER_STATES["AWAITING_STARS_AMOUNT"]}"
                        WHERE user_id = "{message.from_user.id}"
        ''')
        con.commit()
        await bot.send_message(message.chat.id, 'Пожалуйста, введите ниже количество звезд, которое вы хотите приобрести\n\n<b>Минимальное количество - 50 звезд🌟</b>', parse_mode="HTML")
    except Exception as e:
        await bot.send_message(message.chat.id, 'Произошла ошибка, пожалуйста, попробуйте позже еще раз.')

@bot.message_handler(commands=['support'])
async def support(message: types.Message):
    await bot.send_message(message.chat.id, '<b>🧾Вас приветствует поддержка NestxStar.</b> <i>Введите свое обращение ниже строго по форме:\n\n1. Юзернейм\n2. Текст обращения</i>\n\n<tg-spoiler>После того, как ваше обращение будет зарегистрировано, ожидайте ответа в личные сообщения от @Neestxx в течение 24 часов</tg-spoiler>', parse_mode="HTML")
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES['AWAITING_SUPPORT']}"
                    WHERE user_id = "{message.from_user.id}"
                    ''')
    con.commit()

@bot.callback_query_handler(func=lambda call: call.data == 'support')
async def inline_support(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, '<b>🧾Вас приветствует поддержка NestxStar.</b> <i>Введите свое обращение ниже строго по форме:\n\n1. Юзернейм\n2. Текст обращения</i>\n\n<tg-spoiler>После того, как ваше обращение будет зарегистрировано, ожидайте ответа в личные сообщения от @Neestxx в течение 24 часов</tg-spoiler>', parse_mode="HTML")
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES['AWAITING_SUPPORT']}"
                    WHERE user_id = "{call.from_user.id}"
                    ''')
    con.commit()

@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = {str(message.from_user.id)}').fetchone()[0] == USER_STATES["AWAITING_SUPPORT"] and message.text != '/cancel')
async def support_message(message: types.Message):
    await bot.send_message(SUPPORT_CHAT_ID, f'Зарегестрировано новое обращение (@Neestxx):\nЮзернейм пользователя: <code>{"@" + message.from_user.username if message.from_user.username else "tg://user?id=" + str(message.from_user.id)}</code>\n<code>Текст обращения: {message.text}</code>', parse_mode="HTML")
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES["DEFAULT_STATE"]}"
                    WHERE user_id = "{message.from_user.id}"
                    ''')
    con.commit()
    await bot.send_message(message.chat.id, '<b><i>✅Ваше обращение было успешно зарегистрировано. Ожидайте ответа.</i></b>', parse_mode="HTML")

@bot.message_handler(commands=['cancel'])
async def cancel(message: types.Message):
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES["DEFAULT_STATE"]}"
                    WHERE user_id = "{message.from_user.id}"''')
    con.commit()
    print(cur.execute(f'SELECT user_id, state FROM Clients WHERE user_id = "{message.from_user.id}"').fetchall())
    await bot.send_message(message.chat.id, '<b>✅Вы успешно вернулись к началу</b>', parse_mode="HTML")

@bot.message_handler(commands=['balance'])
async def check_balance(message: types.Message):
    user_balance = cur.execute(f'SELECT balance FROM Clients WHERE user_id = "{message.from_user.id}"').fetchone()[0]
    await bot.send_message(message.chat.id, f'<b>На данный момент ваш баланс составляет</b> <code>{user_balance} звезд</code>', reply_markup=markup_for_balance, parse_mode="HTML")
    #CДЕЛАТЬ КНОПКУ С ВЫВОДОМ

@bot.callback_query_handler(func=lambda call: call.data == 'close')
async def close_balance(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, text='Баланс был успешно скрыт')
    await bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data == 'profile')
async def profile(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.delete_message(call.message.chat.id, call.message.id)
    username = (call.from_user.first_name if call.from_user.first_name else call.from_user.id)
    user_balance = cur.execute(f'''SELECT balance FROM Clients WHERE user_id = {call.from_user.id}''').fetchone()[0]
    created_date = cur.execute(f'''SELECT create_date FROM Clients WHERE user_id = {call.from_user.id}''').fetchone()[0]
    success_purchases = cur.execute(f'''SELECT success_purchases FROM Clients WHERE user_id = {call.from_user.id}''').fetchone()[0]
    await bot.send_message(call.message.chat.id, f'*👤Ваш профиль:*\n\n💫Юзернейм пользователя: `{username}`\n🛍Успешных покупок: `{success_purchases}`\n🎁Баланс: `{user_balance} звезд(-а)`\n⌛️Дата регистрации в боте: `{created_date}` ', reply_markup=keyboard_for_transaction_history, parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == 'transaction_history')
async def transaction_history(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    purchases = cur.execute(f'''SELECT amount, time FROM Purchases WHERE user_id = {call.from_user.id}''').fetchall()
    if purchases:
        msg = ''
        for purchase in purchases:
            p = f'💫Сумма: `{purchase[0]} звезд`\n⌛️Время покупки: `{purchase[1]}`\n\n'
            msg += p
    else:
        msg = '🛍У вас еще нет покупок!'

    await bot.edit_message_text(text=msg, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard_for_back_to_profile, parse_mode='MARKDOWN')



@bot.callback_query_handler(func=lambda call: call.data == 'close_profile')
async def close_profile(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.delete_message(call.message.chat.id, call.message.id)

@bot.message_handler(commands=['profile'])
async def profile_command(message: types.Message):
    await bot.delete_message(message.chat.id, message.id)
    username = (message.from_user.first_name if message.from_user.first_name else message.from_user.id)
    user_balance = cur.execute(f'''SELECT balance FROM Clients WHERE user_id = {message.from_user.id}''').fetchone()[0]
    created_date = cur.execute(f'''SELECT create_date FROM Clients WHERE user_id = {message.from_user.id}''').fetchone()[0]
    success_purchases = cur.execute(f'''SELECT success_purchases FROM Clients WHERE user_id = {message.from_user.id}''').fetchone()[0]
    await bot.send_message(message.chat.id, f'*👤Ваш профиль:*\n\n💫Юзернейм пользователя: `{username}`\n🛍Успешных покупок: `{success_purchases}`\n🎁Баланс: `{user_balance} звезд(-а)`\n⌛️Дата регистрации в боте: `{created_date}` ', reply_markup=keyboard_for_transaction_history, parse_mode="MARKDOWN")

@bot.message_handler(commands=['newpromo'])
async def create_promo(message: types.Message):
    is_admin = cur.execute(f'SELECT user_id FROM Admin WHERE user_id = {message.from_user.id}').fetchall()[0]
    if message.from_user.id in is_admin:
        await bot.send_message(message.chat.id, '<b>Введите промокод ниже в формате:</b>\n <code>Название, количество звезд, кол-во использований</code>', parse_mode="HTML")
        cur.execute(f'''UPDATE Clients
                        SET state = "{ADMIN_STATES['AWAITING_CREATING_PROMO']}"
                        WHERE user_id = {message.from_user.id}
                        ''')
        con.commit()
    else:
        await bot.send_message(message.chat.id, '<b>У вас нет доступа к данной команде. Если вы считаете, что это ошибка, обратитесь к <code>@Neestxx</code></b>', parse_mode="HTML")

@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = {message.from_user.id}').fetchone()[0] == 'create_promo')
async def creating_promo(message: types.Message):
    try:
        args = message.text.split(', ')
        cur.execute(f'INSERT INTO Promo(promo, amount_promo, max_uses) VALUES("{args[0]}", {args[1]}, {args[2]})')
        cur.execute(f'''UPDATE Clients
                        SET state = "{USER_STATES["DEFAULT_STATE"]}"
                        WHERE user_id = {message.from_user.id}
                        ''')
        con.commit()
        await bot.send_message(message.chat.id, f'Промокод был успешно создан:\n\nНазвание: {args[0]}\nСумма промокода: {args[1]}\nКол-во использований: {args[2]}')

    except Exception as e:
        await bot.send_message(message.chat.id, f'Ошибка: {e}')


@bot.message_handler(commands=['setcourse'])
async def set_course(message: types.Message):
    is_admin = cur.execute(f'SELECT * FROM Admin').fetchone()
    if message.from_user.id in is_admin:
        await bot.send_message(message.chat.id, 'Пожалуйста, выберите валюту', reply_markup=keyboard_for_course)
    else:
        await bot.send_message(message.chat.id, 'У вас нет доступа к данной команде. Если вы считаете, что это ошибка, обратитесь к @Neestxx')

@bot.callback_query_handler(func=lambda call: call.data in ['change_usdt_course', 'change_ton_course', 'change_star_course'])
async def change_course(call: types.CallbackQuery):
    if call.data == 'change_usdt_course':
        await bot.answer_callback_query(call.id)
        cur.execute(f'''UPDATE Clients
                        SET state = "{ADMIN_STATES["AWAITING_USDT_COURSE"]}"
                        WHERE user_id = {call.from_user.id}
                        ''')
        con.commit()
        await bot.send_message(call.message.chat.id, 'Пожалуйста, укажите курс USDT ниже (целое число)')
    elif call.data == 'change_ton_course':
        await bot.answer_callback_query(call.id)
        cur.execute(f'''UPDATE Clients
                        SET state = "{ADMIN_STATES["AWAITING_TON_COURSE"]}"
                        WHERE user_id = {call.from_user.id}
                        ''')
        con.commit()
        await bot.send_message(call.message.chat.id, 'Пожалуйста, укажите курс TON ниже (целое число)')
    elif call.data == 'change_star_course':
        await bot.answer_callback_query(call.id)
        cur.execute(f'''UPDATE Clients
                        SET state = "{ADMIN_STATES["AWAITING_STAR_COURSE"]}"
                        WHERE user_id = {call.from_user.id}
                        ''')
        con.commit()
        await bot.send_message(call.message.chat.id, 'Пожалуйста, укажите курс звезд ниже (плавающее число)')

@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = {message.from_user.id}').fetchone()[0] == 'usdt_change')
async def change_usdt(message: types.Message):
    course = message.text
    cur.execute(f'''UPDATE Exchange_rate
                    SET USDT = {course}
                    ''')
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES["DEFAULT_STATE"]}"
                    WHERE user_id = {message.from_user.id}
                    ''')
    con.commit()
    await bot.send_message(message.chat.id, f'Курс USDT был успешно изменен на {course} рублей')

@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = {message.from_user.id}').fetchone()[0] == 'ton_change')
async def change_usdt(message: types.Message):
    course = message.text
    cur.execute(f'''UPDATE Exchange_rate
                    SET TON = {course}
                    ''')
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES["DEFAULT_STATE"]}"
                    WHERE user_id = {message.from_user.id}
                    ''')
    con.commit()
    await bot.send_message(message.chat.id, f'Курс TON был успешно изменен на {course} рублей')

@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = {message.from_user.id}').fetchone()[0] == 'star_change')
async def change_usdt(message: types.Message):
    course = message.text
    cur.execute(f'''UPDATE Exchange_rate
                    SET STAR_COURSE = {course}
                    ''')
    cur.execute(f'''UPDATE Clients
                    SET state = "{USER_STATES["DEFAULT_STATE"]}"
                    WHERE user_id = {message.from_user.id}
                    ''')
    con.commit()
    await bot.send_message(message.chat.id, f'Курс звезд был успешно изменен на {course} рублей')


@bot.message_handler(commands=['course'])
async def check_course(message: types.Message):
    ton, usdt, stars = cur.execute(f'SELECT * FROM Exchange_rate').fetchone()
    await bot.send_message(message.chat.id, f'Курс на сегодня:\n\n💎TON: {ton}руб.\n💲USDT: {usdt}руб.\n💫Звезда: {stars}руб.')

@bot.message_handler(commands=['mail'])
async def mailing(message: types.Message):
    admins = [user[0] for user in cur.execute(f'SELECT user_id FROM Admin').fetchall()]
    if message.from_user.id in admins:
        cur.execute(f'UPDATE Clients SET state = "{ADMIN_STATES["AWAITING_FOR_MAIL"]}" WHERE user_id = "{message.from_user.id}"')
        con.commit()
        await bot.send_message(message.chat.id, '<b>👥Пожалуйста, введите текст рассылки ниже\n❗❗Внимание, рассылка будет отправлена всем пользователям, зарегистрированным в боте</b>', parse_mode="HTML")
    else:
        await bot.send_message(message.chat.id, '<b>У вас нет доступа к данной команде. Если вы считаете, что это ошибка, обратитесь к <code>@Neestxx</code></b>', parse_mode="HTML")

@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = "{message.from_user.id}"').fetchone()[0] == ADMIN_STATES["AWAITING_FOR_MAIL"])
async def start_mailing(message: types.Message):
    text = message.text
    cur.execute(f'UPDATE Clients SET state = "{USER_STATES["DEFAULT_STATE"]}" WHERE user_id = "{message.from_user.id}"')
    con.commit()
    chat_ids = [user[0] for user in cur.execute('SELECT chat_id FROM Clients').fetchall()]
    print(chat_ids)
    counter = 0
    text_for_admin = await bot.send_message(SUPPORT_CHAT_ID, f'Начинаю рассылку: 0/{len(chat_ids)}')
    for chat in chat_ids:
        counter += 1
        await bot.send_message(chat_id=chat, text=text)
        await bot.edit_message_text(chat_id=text_for_admin.chat.id, message_id=text_for_admin.message_id , text=f'Начинаю рассылку: {counter}/{len(chat_ids)}')

    await bot.reply_to(message=text_for_admin, text=f'<b>📊Статистика:</b>\n<b>👥Кол-во пользователей:</b> <code>{counter}</code>\n<b>Текст рассылки:</b> <i>{text}</i>', parse_mode="HTML")

@bot.message_handler(commands=['stats'])
async def stats(message: types.Message):
    admins = [user[0] for user in cur.execute(f'SELECT user_id FROM Admin').fetchall()]
    if message.from_user.id in admins:
        users = [user[0] for user in cur.execute('SELECT user_id FROM Clients').fetchall()]
        success_purchases = sorted([int(i[0]) for i in cur.execute('SELECT success_purchases FROM Clients').fetchall()], reverse=True)
        top = (success_purchases[0], success_purchases[1], success_purchases[2])
        top1 = [i[0] for i in cur.execute(f'SELECT user_id FROM Clients WHERE success_purchases = {top[0]}').fetchone()[0]]
        top2 = [i[0] for i in cur.execute(f'SELECT user_id FROM Clients WHERE success_purchases = {top[1]}').fetchone()[0]]
        top3 = [i[0] for i in cur.execute(f'SELECT user_id FROM Clients WHERE success_purchases = {top[2]}').fetchone()[0]]
        await bot.send_message(message.chat.id, text=f'<b>📊Общая статистика:</b>\n<b>👥Кол-во пользователей:</b> <code>{len(users)} человек</code>\n<b>🛍️Всего покупок:</b> <code>{sum(success_purchases)}</code>', parse_mode="HTML", reply_markup=markup_for_stats)


@bot.callback_query_handler(func=lambda call: call.data == 'check_top')
async def top_users(call: types.CallbackQuery):
    success_purchases = sorted([int(i[0]) for i in cur.execute('SELECT success_purchases FROM Clients').fetchall()], reverse=True)
    if success_purchases:
        top = (success_purchases[0], success_purchases[1], success_purchases[2])
        top1 = cur.execute(f'SELECT user_id FROM Clients WHERE success_purchases = {top[0]}').fetchone()[0]
        top2 = cur.execute(f'SELECT user_id FROM Clients WHERE success_purchases = {top[1]}').fetchone()[0]
        top3 = cur.execute(f'SELECT user_id FROM Clients WHERE success_purchases = {top[2]}').fetchone()[0]
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>🏆Топ 3 пользователя бота\n1.\n|\n|\n----</b><a href='tg://user?id={top1}'\>{top1}</a><b>\n     |\n      ----</b><code>{top[0]} покупок(-и)</code> \n\n<b>2.\n|\n|\n----</b><a href='tg://user?id={top2}'\>{top2}</a><b>\n     |\n      ----</b><code>{top[1]} покупок(-и)</code> \n\n<b>3.\n|\n|\n----</b><a href='tg://user?id={top3}'\>{top3}</a><b>\n     |\n      ----</b><code>{top[2]} покупок(-и)</code> \n\n", parse_mode="HTML")
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<b>❌Еще не было совершенно ни одной покупки</b>', parse_mode="HTML")

@bot.message_handler(commands=['newadmin'])
async def new_admin(message: types.Message):
    admins = [user[0] for user in cur.execute(f'SELECT user_id FROM Admin').fetchall()]
    if message.from_user.id in admins:
        cur.execute(f'UPDATE Clients SET state = "{ADMIN_STATES["AWAITING_FOR_NEW_ADMIN"]}" WHERE user_id = "{message.from_user.id}"')
        con.commit()
        await bot.send_message(message.chat.id, '<b>Введите ID пользователя</b>', parse_mode="HTML")
    else:
        await bot.send_message(message.chat.id, '<b>У вас нет доступа к данной команде. Если вы считаете, что это ошибка, обратитесь к <code>@Neestxx</code></b>', parse_mode="HTML")

@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = "{message.from_user.id}"').fetchone()[0] == ADMIN_STATES["AWAITING_FOR_NEW_ADMIN"])
async def add_admin(message: types.Message):
    try:
        admin_id = int(message.text)
        cur.execute(f'INSERT INTO Admin(user_id) VALUES({admin_id})')
        await bot.send_message(message.chat.id, f'Пользователь <code>{admin_id}</code> назначен администратором', parse_mode="HTML")
        cur.execute(f'UPDATE Clients SET state = "{USER_STATES["DEFAULT_STATE"]}" WHERE user_id = "{message.from_user.id}"')
        con.commit()
    except Exception as e:
        await bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['deladmin'])
async def del_admin_state(message: types.Message):
    admins = [user[0] for user in cur.execute(f'SELECT user_id FROM Admin').fetchall()]
    if message.from_user.id in admins:
        cur.execute(f'UPDATE Clients SET state = "{ADMIN_STATES["AWAITING_FOR_DELETE_ADMIN"]}" WHERE user_id = "{message.from_user.id}"')
        con.commit()
        await bot.send_message(message.chat.id, f'<b>Введите ID пользователя</b>', parse_mode="HTML")
    else:
        await bot.send_message(message.chat.id, '<b>У вас нет доступа к данной команде. Если вы считаете, что это ошибка, обратитесь к <code>@Neestxx</code></b>', parse_mode="HTML")

@bot.message_handler(func=lambda message: cur.execute(f'SELECT state FROM Clients WHERE user_id = "{message.from_user.id}"').fetchone()[0] == ADMIN_STATES["AWAITING_FOR_DELETE_ADMIN"])
async def delete_admin(message: types.Message):
    try:
        admin_id = int(message.text)
        if admin_id == 1451835695:
            await bot.send_message(message.chat.id, f'<b>Хуй тебе</b>', parse_mode="HTML")
        else:
            cur.execute(f'DELETE FROM Admin WHERE user_id = {admin_id}')
            await bot.send_message(message.chat.id, f'Пользователь <code>{admin_id}</code> был успешно удален', parse_mode="HTML")
            cur.execute(f'UPDATE Clients SET state = "{USER_STATES["DEFAULT_STATE"]}" WHERE user_id = "{message.from_user.id}"')
            con.commit()
    except Exception as e:
        await bot.send_message(message.chat.id, f'Ошибка: {e}')


#основная функция для запуска бота
async def main():
    await bot.infinity_polling()

if __name__ == '__main__':
    run(main())
