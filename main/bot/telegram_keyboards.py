from telebot.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, WebAppInfo
from url import url_for_rules_app


#клавиатура после проверки на подписку
markup_for_inline_keyboard = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton('📜Правила', web_app=WebAppInfo(url=url_for_rules_app))
btn2 = InlineKeyboardButton('🛒Купить звезды', callback_data='buy_stars')
btn3 = InlineKeyboardButton('🎫Промокод', callback_data='promo')
btn4 = InlineKeyboardButton('🛠️Поддержка', callback_data='support')
btn5 = InlineKeyboardButton('👥Профиль', callback_data='profile')
markup_for_inline_keyboard.row(btn1)
markup_for_inline_keyboard.row(btn2)
markup_for_inline_keyboard.row(btn3)
markup_for_inline_keyboard.row(btn4)
markup_for_inline_keyboard.row(btn5)

#клаиватура для проверки на подписку
markup_for_subscribe = InlineKeyboardMarkup()
bt1 = InlineKeyboardButton('Подписаться на канал', url='https://t.me/+DbuiDxmi3-FlY2Yy')
bt2 = InlineKeyboardButton('Готово', callback_data='success_subscribe')
markup_for_subscribe.row(bt1)
markup_for_subscribe.row(bt2)

#основная клавиатура для команды /menu
markup_for_main_keyboard = ReplyKeyboardMarkup()
b1 = KeyboardButton('Правила', web_app=WebAppInfo(url=url_for_rules_app))
b2 = KeyboardButton('Купить звезды')
b3 = KeyboardButton('Промокод')
markup_for_main_keyboard.add(b1, b2, b3)


#клавиатура для оплаты (отмена или подтверждение)
markup_for_buy_keyboard = InlineKeyboardMarkup()
markup_for_buy_keyboard.row(InlineKeyboardButton('🛒Купить', callback_data='buy_approve'))
markup_for_buy_keyboard.row(InlineKeyboardButton('❌Отмена', callback_data='buy_cancel'))

#клавиатура для действий с балансом пользователя (звезды)
markup_for_balance = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Вывести', callback_data='get_stars')
button2 = InlineKeyboardButton('Закрыть', callback_data='close')
markup_for_balance.row(button1)
markup_for_balance.row(button2)


#клавиатура для выбора валюты
keybord_for_assets = InlineKeyboardMarkup()
k1 = InlineKeyboardButton('💲USDT', callback_data='USDT')
k2 = InlineKeyboardButton('₽RUB', callback_data='RUB')
k3 = InlineKeyboardButton('💎TON', callback_data='TON')
keybord_for_assets.row(k3, k2)
keybord_for_assets.row(k1)

#клавиатура для просмотра истории заказов
keyboard_for_transaction_history = InlineKeyboardMarkup()
kbth = InlineKeyboardButton('История покупок', callback_data='transaction_history')
kbth2 = InlineKeyboardButton('Закрыть', callback_data='close_profile')
keyboard_for_transaction_history.row(kbth)
keyboard_for_transaction_history.row(kbth2)

keyboard_for_back_to_profile = InlineKeyboardMarkup()
kbfbtp = InlineKeyboardButton('Назад', callback_data='profile')
keyboard_for_back_to_profile.row(kbfbtp)

keyboard_for_course = InlineKeyboardMarkup()
kfc1 = InlineKeyboardButton('💲USDT', callback_data='change_usdt_course')
kfc2 = InlineKeyboardButton('💎TON', callback_data='change_ton_course')
kfc3 = InlineKeyboardButton('₽RUB', callback_data='change_star_course')
keyboard_for_course.row(kfc3, kfc2)
keyboard_for_course.row(kfc1)

markup_for_stats = InlineKeyboardMarkup()
kfs = InlineKeyboardButton('🏆Топ пользователей', callback_data='check_top')
markup_for_stats.row(kfs)