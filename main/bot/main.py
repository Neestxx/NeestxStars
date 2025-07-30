import sqlite3
from telebot.async_telebot import AsyncTeleBot
from telegram_keyboards import markup_for_inline_keyboard, markup_for_subscribe, markup_for_main_keyboard, markup_for_buy_keyboard, markup_for_balance, keybord_for_assets, keyboard_for_transaction_history, keyboard_for_back_to_profile, keyboard_for_course, markup_for_stats
from asyncio import run
from telebot import types
from url import start_message_pic, buying_picture
from aiosend import CryptoPay
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fragment_requests import Fragment
from telebot.util import is_command

bot = AsyncTeleBot('7765752506:AAEiOlH4r9WPcg9jGwC5idENGxNzen2i5DA')
cb = CryptoPay(token='405874:AAHkdWpYVCQu8bfqRHMukLtFxSlTti6neOm')
fragment_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzc3QiOiI2NzQxNDE0MTQxNDE0MjZmNjgzOTZkNGU0YjRkNGY3NTQ1NjU2MjU5NmQ1NDJkNzQ1MTczNjY2YzVmNmQ0ZTU0NGE1NTRjNzQ3MDU0NDY0ZTc3NTMzNzYyNTI3NjRjNDU0NTQxNzg2YTZkNTA2NjcxNmQ1MjZkNDY1YTRhNWY0MTMyNmUzNjQ0NmQ0MTMyNzA3NDU4NWE3ODUwMzc2ZDMzNGM0ZDRiMzk0OTZhNGM3MTZlNmU3NjRjNDk0ODRmNDM0ZTQ3Njk3MzQxNzE1MDM5NmQ3ODQxNGYzOTU5Njc0ZjRiNzU0ZDY0NjM2NzcyNGM1ODVhMzAzMTQ5NmY2NTcyMzM1OTRiNzI0NTM5NzM3NTQ5NTY0OTZkNzQ1NDczNTg1NDRlNmM3MzY0NGU1ZjZlNzc0ZTYyNGY0NzU4NDI1NDY5NDU1NjcwNGQ0NDQzNWY2MTZkNmUzMDUwNTY3NTUwNzk0ZDc3NGEzOTRkNTY0NzY3NmY1NjUwNjEzNTUyNmM2NzU2MmQ2NjMzNDk1NjdhNzY2YjUyNTQ2MjM5NzE2MzUwNzI2OTRjMzAzNTYzNmYyZDYxMzM0ODMwNGM3MTQ5NzA1MTQ2NTM0YjY3NGQ0ZTM5NjkzMTMxNmIzMDc0NzQ2ZjQ2NmI1MTUyNmQzOTc5Njk3NjM0NDk1NDM0MzA2NDZhNmIzNDJkNmE2YjY4NGM3MjZkMmQ2ODQ1Nzc2MjczMzgzNDZkNjg0ZjRlNjI2Njc3NzE1NDYzNzY1ODY0NDY1MTM5NTg1OTRlNjI2YTY5NjI2NjcxNGIzMTY0NDEyZDM2NGM0YzQyNGYzMjRiMzU2ODQ1NDczOTQ3NTE0OTMxMzk0YzU0Njc2YzczNmIzMTYxNDMzOTU2NzA2ZTZlNmI2NjZkNmM0ZDM0NjE0ZTM2NGI1NzUxNGU3NDY4NjY0MTQyNzY3OTcwNTI0ODcwNzA0YjRjNTI2OTU0NmMyZDJkNmI1MjMxNTYyZDY2NTQ0MjMzNmI3OTcyNDQ3MzQ1Njg2ZjM4NWY2ODU1NjM3MDQ4NzA2ZTMyNmE0ZDMwNDM3ODY1NjY1MTRjNDY1NDM3NzY1Njc5NWYzMDMyMzM2MjYxNGE3NzQzNmM3OTQ0NmQ0YzQ0NzU2NTQ5NTkzNDY3Nzc1OTVhNzQ3MjQ2NjI2OTZjNmY3NDMyNDU2ZjRiNmQzMDVmNTkzMjc1NjQ1YTU2MzY2MTJkMzc0NjZjNjM3NzU3NTM0NDRkNDI2YjQ0NWY1NTU3NjMzNTY3Njk3MDM2NGEzOTZjNTE0ZDMxNDk1MjZhNGE3YTQ0NjE1ZjU3NmI1NzQ2NDU1MjQzNDY2YzUzMzQ1MTUyNWYzODc0NzM3NzVhNzc2NjZjNDc2ZDQxNzE1ZjcyNzM2NzM0NDIyZDQzNDM0ZTQ1NGY0ODYzNjIzODc0NmY2ZDRiNDczNTY0NGM1MTYxNTU3MTQxNmYzODcxNTA1OTU5NGE2OTY5NTg0NTYzNTY0NzU2NTU1OTRmNzIzNjU0NzY2ODUyNDc1NTU2Nzc2MTU5NmYzMzU0NWEzMjU4MzY0ZTU4NTA0ZTM0Njg1OTM0NDU0OTc2Nzc0YjQ1NjQ1NjM2NjI1NjRkNjg2ZDY0NTg0ZjdhNDk2NTYzNjM0MzVmNzEzNzRmNTE1ODcyNmMzMTZlNTc1MzYyNzg2ODYzNGM0NDMyNmE2ZTc1NzE0MjQ3MzQ2YjUxNDQ0MjZlMzI2MTM2NTI0YjQ3NTI3MjQ3NTczMTMyNGMzNjQ0NDg2ODM5NjEzMjYxNzk0ZjUyMzIzMDUyNzAzMTM3MzgzMDYxNDE2YTc1NmU3NjcyNjkzNDZlN2EzMzRmNDI2NjcxNmE0NTU3NmM0YTZlNmYzMTY0NTI0NDMwNzU0YTQ3Mzg2YjM4NzE1NDcxNTE1MTQ4NzE0ZjY3MzU3MzQ0NjgzNTMyNmM0NjQxNjczMzQ5NTM1YTY3NTkzODU5NTk1ZjUxNTE2ZTc5Njc0MjZlNjU0YzUyNjc1MTZlNjU1MjUyNDI0YjMxNmEzMjRkNTI0OTcxN2E0ZTMyMzQ2NzVmNDk0OTU0NzM2YTZkNmY3MjQxNmY2ZjM5Njg0MTQzNTQ0YjU0NGM3MDQ3NDc2YzVmMzY0YTY5NjE0ZjY5NDY2ODRhNGU2YjRkMzI2YTMxNTg2YzY1Nzk0MjdhNGQ0YTU0NzEyZDRiNTM0NTc2NTI2NjU0NGE0NzZlNDM2MzM1NzI3ODU0NjE3NzYzNzc3NzU3MzczMjUzMzM1NDU3NmY2NzM4MzY3MTczNjc1ODcwMzQ0ZTcwMzg2NDQxNTA3ODVhNjk1MTY1NWY0OTQ5Njg1ZjQ1NDI2ZTcwNmI2OTUyNzc0YTU3NmMzMTcyMzg1NTRjNTA0ZTMwNDQ2ZjQ3MmQzMTdhNDE0MzY5MzA2MzYyNGI0ZjM4Njg1ZjQ1MzM0ZjcxMzIzOTQ2NmU0NTY4NDM3Mjc5NDM2NTU2Njg2MTQ2MzE0MzRiNGE2NTU0NTg0ZjM4Njg2OTZjMzM1NjcxNTA0MTZkNDQzMTU5NmM0OTU3NmE3OTY3NzI0ZjZjNDI2NzQ5Nzg1OTZjNTU3ODQ0N2EzMjc5MzA1MzU5NzU3MzRiMzkzNzUyNjU2OTQ3MzQ2NzU0NGMzNTc0NzQ1NjY2NDI3YTU1MzgyZDQ5NGY0MjYzNjU3NTczNjg0NTU0N2E1OTM1NTY0ZDY1NGE0ZTQ1NmU2ODM5NGY3NTM3Mzg3ODMyNzI0NzUyNGY3NzYzNGIzNDM2Mzg2ZDcxNDY1NDczNjc1NzRmNzgzMjY3Mzg0ODY0N2E2NzQ3NTg0NTQ5Mzk2NTZiNWY0ZDM2Nzk0MjM5NGE1MDc4NDU1MTYzMzk2OTc0NDU2NTMzNTk0ODcxNjU2MzcwNzk0MjMzNjU0ZjQ0NTI0YTYzNDczODJkNDc1ODQ0NGU1MDQ2NzY3NDRkNGY2OTRkNTU1MjQ5NTkzNjQzNTg2MzRiNmY3NjUwMzg0YTVmNTA2NzcwNjI1NzQ1NTk1ODYyNGI2MjMyNDM1NzMwNjQ1OTcyNTc1NTczN2E3MjRkNjY0OTU2NTc0OTVhNjUzMDQ4NzI1ZjMyNjgzMzZiMzg1MjZmNTQ1MDZiNDM1ZjM3NWY1MzY1NzA2NzZhNTE2ZTQ2NDc0MjVhNjI3NDRkMzA1NDcxNjU1Zjc0NWY1NzZlNTM1NTYxMmQ3MDY3Nzc2NDY1NDM0NTVhNjM1Mzc4N2E3YTVhNzg0NTZkNDY0ZjU4Nzg1ZjU4NWY0YzU2NjI2ZDZmNGE3MDJkNmQ2ZDc3NmMzMjY1NDEzMTZhMzg3NzY1NDI0ODZiNjI2Mzc0NmY0NzY0NTAzMzc5NjY0NTU5N2E0YzMxNjgzODcxMzI0ODc3MzM2OTU4NmQ0ZTc4Mzk0MjU2NDk0ZjcwNjMzNDVhNTg3MDc3NTE3NDUzNWE0MzY1NGI3NzUxNDU2ZjY1MzIzNjY1Nzk2MjQ1NjY3NTQzMzc2YzY0NDk3Nzc0NzU0NzQ1NzQ3NTQ2NDY0ZDM5NTg2OTM2NTE0ZTVmNGMzNTZjNTM0NDRhNDgyZDU5NTA0MTM5NjY0YjY1NTQ0NzRiMzc0NTZiNDY1ODRiNjQ0YzQ2NDc0YjYxNjYzNTc3NGQzNDU1NTY0NDZiNmE0NDMzNzQ0NTcwNmU0ZDc5NTM0OTY3MzAzMDQzNWE2NTQzMzgzNjQ2Nzg2ODZmNmEzNDZhNmY3YTVmMzY1NzZkNDE0NjUxNjM1MTY5NmI1MTZlNjgzNTM5NTE2ZTY1NDQ2NDc3Mzk0YjcwNjI3YTYyNmQzMzU0MzQ0NTcyNjI3ODRlNmYyZDM2NzU2YjRmNjQ2ZTc1NGQ0ZTdhNDI0ZDQ5NmM2ZTMzNGI1MzQ4NzY2NjY2NDY2YzY0NTc2MzMyNzg0NzY2NmM2MTM3MzA1NjYxNWEzNzU2NjQ1NDc3MmQ1MjRkNTA2YzUyNjQ0YjJkNmI0ZTMyNDg0ZjQ5NmM0MTY3NWE1ODU5MzQ2MTU4NTk0NzYzNGM2NTM0NzY2NTc3NDI0NDM3Njk0YzVmMzY0YTczNDI3YTcxNjU2MTczMzg0OTRjNzQ1OTMzNzUzNTM1NjI0MjQ0NzYzMjQ4NjY1NTU2NWE3MjQ0MzY2OTc1NjY2ODU0NzIzNTczNDg0ZTQzMzc2NjZjNmQ3OTUxNTc2YjUyMzk3MTc2Mzk1NTQ0NDk2ZjdhNjQ2NDRlNGIzODZlNDYzMTQ5NWY0NjU5NGY1YTczMzU1MzQxMmQ0NjQxNzk3OTM3NzQzMjRiNTY1ODUwNzE1MTcwNDU2MzUwNTQ2YjRmNWE2ODcyNmM0MzZkNGQ2MzMzNGU0ODQ2NGI0ZjU4MzQzNzM4NTc0OTczNGI0ZTRjNzU2NDU1NjM0MTM5NzU2YTMzNjI1MDZiMzc0ZDY2NDM0NTUyNzM0OTRiN2E0NTc1NTc1OTc0NDk1NDZjNzIzNjMwNjY0ODc1NDk2YTYxNGI0MzRkNDM0NDU0NTgzMjUzNDg1MjZkNGQ1YTU1MzA2OTUzNTA2MTY2NzM0NzQ1MzY3MzY5NDQ2MzUyNjc2ZTZmNGEyZDdhMzc1ZjU3NjQ2Yjc2NmM0ZDM4NDg3MDQxNjI3MDU1NGY0OTc4N2EzNjM4NjQ1NTM1NDI2NzY0NTk1NjQ3MzY3MzcwNTYyZDQ4NGU1Zjc2NTg2YjRkNWY1YTZiMzc3NDY2NDU0YzUxNDg2MjYxNjE3NTQzNTAzMDU2NDM0MzcwNDMzNTY3NzMzNzQxNTU3MzU5NTczMDRjNjk2ZDY5NjI1OTYxNjUzMzMwNjg3MTJkNzI2ZDVhNzg0OTY5Mzc1NzYzNjE3Njc1NmY1ODQxMzE0OTQ2MzU0ZDY4Mzk1NTUxNzczMjRlNmQ0Njc1NzczMDUyMmQ3YTMxNjMzOTM3NjU2YzQxNzU1OTZlNzQ1YTM5NGY0NTc3MzA1ZjRkNjQ2YzUxMzQ2NzZmNzQzOTUyNzYzMTQ2NTU2NzYzNjY2ZjcxNjEzMTU2NzgzNTZmMzI1ODcxNWY2MjUyNGQ1ZjU2NGMzMjQ0NGY0NTcwNjc3MTU2MzQzMzc0NTY0NTc1NmMzNDQxNTE2NzUzNjE2ODQ4NmM2NjQ5NTA0OTU3NGY1MjU1NGY1MDUzNzIzMzM2NTY0YzUxNDQ2NTcyNDk0YjRlNzYzOTMxNzE1OTQyMzE1NDRlNDU2NTZlNjM2ODM5NjkyZDY0NzM0ZDRmNmI1ZjRkNGM2ZDMyMmQzMzc2N2E1NjJkNzM1NzZkNGI3OTM2NjQ0ODc2NTM0ZDUwNTg0MzY0Njc1NTcxNGQ3MjZkNTI2NDc3NDk3NzQyNmM0MTUxNjk2NzczNjc0YTc4NGM1NjVmNzA0YTQ4NmU3NjRkNDM3NDQ3NTI1NjJkNGY1NzVmNzg0YjMxNzI1MTZmNzc2Mzc3NjY1NDQ4NGYyZDY0NDI3MTQxNDY0NzZmNTQ3YTYzNTgzMTJkNDE3NTU5NmIzNTQ3NTk3NzU0NzI1NzRmNTk2ODU5NzE3ODQxNGU2ZjM2NjU2ZTM1NjU3NTY3NGM1MzZmNTkzOTQ1NTUzODM3MzI0NDMxNmU1ODMzNGQ0NDM0MmQ2NTc2NmY2ZTdhNzIzMDc1MzQ1OTYzNDEzNTVmMzczMzRmNzE0MTYxNzMzMzczNGI2NzU3NTg3MDY4NmY2Mjc3MzczMzJkNmY1NTZiNzE1ZjQ5NDE0MTc4NjQ1MjMzNzA0MzZlNjg2YjQ4MzQ3ODM4NTM1OTYzNmU0Yjc2NTQ0ZDUyNGE0YjMxNzQ2OTM0NmQ1MTMwNjE3ODc3NTk2NDRjNmE1NDUxNzA2MjM3MzI2NTU3NmY2MzRkMzA2NDRlMmQ0ZTQxNzAzNzYyNmE0OTMyNWY2OTQyNTc0YjcwNjk2ZTc4Nzc2NzMxNzI3MjY5MzY2MTYyNDQ1OTUyMzkzMzcxNmMzNzMyNzgzOTM1NmE1MDRmNTkzMjYzNTU0ZDc3NzEzMDMyNDk0YzYxNGE3NjY1NmY2NTZkNmI3MzVmNGI3NjQzNmY1NTQzNzc2MTQ0NDEzODY1NDM2NjU4Nzg1NDRiMzc1MjRkNTk2ODRhMzYzMjVhMzI3MDMyNDE0Njc4NTYzMjU2NzQzNTU4NTg0OTc5Nzk1ODZmNjk3YTRmMzc1NDU0NzM2Yjc1NjQ2YzUyNjg2NTM3NjY3NjY2NTM0YTUzN2E2ZDcxNWYzMjcyMzk1MzM1NDY3OTQ0NGUzMzU4MzI2ZTQyNDc2NDQ0NWYzMDM1NmU1ZjMxMzk3NzRiNjY0ZDM3NGI0MjM2MzY1NjM4NjI1NDYyNzk2YzU4NGU2YTZjMzE3NjM2MzU2ODZmNDQ2YjM2NTQ3NjZiMzA0NTQ5MmQ1YTczNjQ0MjQ5MzQ0NjQxNzg3NjUwNjE3NTZhNDI0YjJkNjk1NDcxNTc1MjQzNmM2ODQ1NmU0MzUzNzAzMDVhNDQ2Yjc3Njc2NjczNWEzMjUxNjI0ODRhMzEzMjRkNmI1MTc1Mzg2YzQ1MzI3NDM3NjQ0MzRiNGQ0NjM2MzM3MDQ4NGY2ZjQ4NTQ3MzRiN2EzNjY5NGI2NjZmMzM2ZTY0Mzc1ODMwNmE2ZTU1NTM2NDQ5NjM1ZjcwNWE3YTM5NGEzMDc3NDM0NjY3NjUzNTM3NTczNzZjMzk2ZjQ2MzQ2MzczNDg3MzQ4NGI1NDMxNmI0MjYxNmQ0ZTU0NzQ1NzY2MzE1NTc4NTU3YTMwNTg0NDU2NmM0ZDRjNDc0Nzc4NjY3NDU1NTc1YTQxNDc0OTY2N2E3MjU3MzI2ODU3NjU0ZjcwNDE2OTU0NjM0NjQ4NDc2ZDZiNzA2ODUyNjczNTczNzY0MTY4NzQ2MjcyNTU3NDZjNmI0OTYzNjI1ZjU0NzI2MTZhNjI1MjU1NDMzMTVmNjU2YTM5NzA3Njc1Nzg1NTU0NzUzODY0N2E2ZjM2NDk2NDMyNzI3MTM5NDgzNjY3NTU1NjU2NDE1YTQ4NDM2NjZjNmM2NTc4NzkzMTU1NzY1ZjY5NmU1YTQyNzEzMjRkNGM0MTQ5MzU0YzY4NDg0MzcyNmEzNDRkNDYzOTY2NTE3NjRkNjc0YTRkNzQ0ZjQ3NjczOTczNWY0ODc2Mzg3NTUyMzM2YTU3NzE3ODRiNTQ0OTc2MzQ0ODRjNTYzNTY2NTA2NTMzNDc3MjRkMzgzNTUyN2E3MzU4NjY2NDYxNDY0OTZiNjkzNDRjNjI0ZTQ0N2E2MjRkNTU0YTVmNjQ1NTY2NjU1ODUxNDM0NDRiMzc0YzUwNTM1MjVmMzE2Yjc4NzA3YTM3NTA1MDVmNTE0MjQyMzY3NzRlNDk3NTc3MzU0YjQ3NjY0ZDM3NmM3NTZiMzgzMDYxNzk2ZjM0NTE2NjVmMzQzNTUwNjM2Njc5NDI2MjQ3NTE1NDM3NjU0MTJkNzM3ODU1Njk2ZjQyNzg0ZjZjNzU0ZDQ4NGI2OTU2NGE2YjZiMzU2ZjcxMzI2YzU5NGY2ZTdhMzI0YTUyNjg2NTUwNmE2ZjJkMzU3NTQ5NTM2MzRhNmYzNTdhNzE0ZTY0NTQ1NTQ1NjE3ODRmNmE1NjUyNTQ2NzUzNjg3YTM5NDkzNTU0NDQ1Njc0NWY3NzQ4NGIzNTYyNDk3MzYxNGQ3ODMzNDY0NzY5NDc1NzUwNDY1NjMwNjc2MTY5Mzg2YjZiNGE3MTc1NDY0YzZiNTEyZDc1NTA1NzY2NGM0NjU3NjMzNzc2Nzg0ODQ4NGU1NDU4NmM2ZDQ2NTU3YTRkNjU0ODVmNmI2MzcxNTIzNDZjNDQ3MjQyMzA0Mzc2NjgzNjVmNDg0MTY2NmY0Zjc2NjU3MDY3NjEyZDRmNTc3Nzc1Mzc1MjUxNGQ2MzczNTc1MjM3MzY0MTU5Njg1MjJkNTUyZDc3NjQzMjRlNTg2Zjc2Njk3MTdhNzg0YTQ5MzI3OTcyNjM3NTUxNTY2NTQzMzM2NDY3NDU2YzMwNzI2ODU3MzY1MDY4NDk2MjU4NTU2YjY1MzM3YTMwNTkyZDQ5NDI1MDU3NDc2YTQ4MzY2ZTRjNmY0NDc0NzM0ZDM5MzgzOTRkNDc2YzM4MzM2ODZjNGU3NTc4NDQ0NDczNzA0ODcwNGY2YjQ4NzQ2ODMzNTEzNzYyNDM1ODc0MzU2YjU1NmE0ZjMyNTYzODQ4NDE0NjczNjI0NDczNTE3MjMzMzI0YjRkNjIyZDU5NTg3MTM3NTk2NTc3NzEzMDczNmI2ZjRkNjI3MjZlMzA1ZjM0NzIzNzcwNzg2ZjMzNGUzMzZhNTY1NDM4NzkzMDYyMzc1MDM1Nzk1NzU0NmI2YjcwNGQ3MzZjNTc0NDYxNzc2MTc0NzQ1MTMyN2E3ODM1NzUzMjZmNGMzMTZiNjU0ODM5NTY2ZjcxMzg0MTc2MzQ0ZTQyNmYzOTQ5MzY2OTY5NmI0NzM2NGY2YTU0NTY0YjM1NzU3MzU0NDQ1NTVhNjQzNTU4NzUzNDM0Mzk1MTcyNzk0YTRjMzk0YTMyNzI0YzY1NzI2ZTM1NjI1ODM3NjY0ZjczNDk0MzYxNzk0NjUzNDg0NTRmNzg2YTRhNmI3YTc4NzA1YTZjNzA0MTQ0MzI1YTMyNmI3NjdhNDIzMzYyNTY3MTYxNDQ0NTJkMzU1YTM3MzU3NjcxMzAzODRhNzI2MzMyNTI2NDY1NmQ1NTYxNmEzNjY0NGY2MjY5NDY0ZTU4Nzc1OTcyNTA2ZDc4Njc2ZTY2Nzk3NjM2MzM2MTc0NDY1MjUxNTQ2YjM5MzI0NjUzMzQ1NDc5NDg2YjQ1NzY2MzY5NDY2ZjM5NTczODY1NmQ2MTYyNDM1NzQ4NmE3NjVmNDU0Njc5Nzc1OTRhNTQ2NjUwNjc1NzZlMmQ1MjM0NGI3ODY3NDY2MTYyNGI2MzQxNTIzNTVhNTY2Yzc2NDM0MjM3NTI2Nzc5NmY3NTMzNzI0MTcwNGI0NTJkNDM0Zjc4NzIzMzQyNjI0ZjM2N2E0NTMyNTQ0OTRkMzU1ODY1NmIzNDMzNGI3MzcxNWY2ZjM5Njk2NjcwNjc2ZTUxNjQ3NTM3Mzc3NjRmNDk2YzM3NmI3MTQ4Njg0Yzc2NjkyZDcyMzM3Mjc4NmM0YzZmNjI0MzQ5NDg0YjMzMzQ2YTQyMzY2ZDZjNjM0ZDQ3NmY0MjQxNDg3OTM1MzU1NzM3NjE1MzUwMzM0YTY0NTQ3NjY1NWY2NDRkNTQzNjczNjE1OTM3NDI1MzY4Nzg2YjRmNmY1OTc5NzkyZDY5NmE0OTcxNTg0NjM5NWY3MjMwNTkzODJkMzQ0ZTMwNGIzNDUxNGQ0OTQxNjEzNTRmNzg3MjVmNTE3NjM1NTM2NzY4MzE3OTRiNTI0OTU3NzU0NjU1NDY0NjU3MzgzNjM5NjQ2ZjQzNmY3NzYzNDE0NDYzNDI2OTc0MzU1ZjY4NGE1NzUyNjM3OTU2Nzk2MTY0NjI2YzQ5NzE2ZjQ0NjQ1NzM2NjQ1NjY4NzM3NDc1NGEzOTMwMzgzNDc5NDU3MjRiNDk1NzMyMzMzNzZkNDg3NjU1Njc1MTY0NjI1MzUzNjU0NDZkNGYzMDY3NzU0MzVmNTc1ZjY0NzQ2NTQyNjI3NzZjNDM2MTMxNDc0YzU5NzY0MjY5NWY0ODJkNmM0ZDU2NWE2ZjZmNDM3NDc3NzU2OTYxNTIzMDZlMzU2MTc5NDg3MTM4MzI2NTYzNjI1MDU2NDc0ODRiNTM1YTM3NTU0YjU4NmYzNjZkNjQ2YjQ1MzQ0ODM1NmE0MzZlNTA0Njc5NzQ0ODc0NmE0MzY5MzQ2NTY3NGMzMjVhMzI2ZTMzNjE2MjU0NzQ1MTYzMzAzNDY0NjUzODY2NzI1MzU3N2E1ODU5NjE2NjU3NzI1MzU5NTQ2ZTc0NTg1MjM0Njg0ZTcxNTM0YjQ3NTQ0ZDczMzE2ODRiNWY3YTYxNDI3NDQyNjk2MzQ3NjQ3MzU4NTE0ZTRkMzA0OTYyMzE2ZTY4MzE0YTZiNzI2MTMyNDE3MzQ3NjI1NTcxNWYzNDZhNjg0ODQ1NzY0NTY3MzM0MjZlNzI1OTQ4Nzc2ZjU1NmY3NTY1NzI2MzU5Nzg1MDY3NTk2YzMxNmMzNzU0NDE1NDczNjg1ZjQ3MzQ0YTUwNDg3NzZiNzc0NzU3Njk0ZDU2NGI2MjZhNjE2YTc0NTg0Mjc4NjU1OTY5NDE3MjcwNDk2OTc3NTQ2NzVmNjg1ODZlMzk2ZDM4NDE2ODY2Njc1NDU1MzE2NjU3NjM0NjU5NGE3NTJkNTY3MTZmNzM0ZDU5MzYzMzQ1NmE0OTU3NzM2ZDMzNmIzMjUwNzY2ODczNTc0NTQyNDE1MzM3NjU0MzU1Njk1ZjZhMzI3MDM3NGM1MjRjNDc0YTM1NmM0YTY5MzMzNzcwNmQ1MTQxNGQzNzY1NjYzMDMzNTU3MjJkNGQ2ODQ2NTY2OTQzNjE0NjZhNTQ3MzY3Nzg1NTVmNmU3YTMxMzU0OTUxNDk1MzRiNDc2ZDVmNGM2ODYzNzY1NjQ2MzgzODc4NGQ3YTZkNjc3YTYzNDU0MzQ3MzY2NDc0MzU1ODY4MzEzMTQ0NjgzMjU1NDM0OTYyNDc0NzU0NzQ1MzJkMzY2YTMwNzI2NTZmMzM0NjZhNDE2ZjM0NTc2YzYxNjk3Mjc0NmI1NjYxNjI3NzZmNmI2YjU1Mzc1Mzc0NzEzODYyNDQ2MTY3NzY0ZTMxNGU2ZjM3MzAzODUzNDU1MzYzNGEyZDZkNDY1YTM3NTczOTM2Nzg2MjdhNjI0ZTY5NmQ0ODY4Mzg1ODQ2NTY2NjQ5NjEzODM4MzE0OTU2NzA0YjU3NjY0YjcyMzI3OTc3NTE3NDRjNTk2MzU3NTI1NzM0Mzg1MTMxNzk3ODc3NTUzMzRhMzc2YTUwMzI0ZTVmNmI1MzRmNzc3MzcxNGU2YjRmNWE1NzU2NTQ3MDU0Njg3Nzc5NmM0NjRjNzEzOTRmNDczNDcyNWE1NTM5NjU2MTRjNDM2NzQ4NDk0ODUzNjE3MDYyNDk0YTRlNDczNzM5NGI3NDM1NmY1ODYzNDI2ZDdhMzQ0NzU5NzQ0NTMwMmQ0ZTVmMzM2MTc5NjM3NTQyNmU1MjU3NzAzMTUzNmE2YjYyNmQ0YTZkMzU3ODQ3MzA2MTc0NDQ2NzY3NzU2MjM2NmU2ZDM5MzMzNDY4NTE1NTU2NjI1ZjM4NTk2ZDJkNmU2NTQzMzU0NDQxMzY3MDVmNjI0ZTZkNjk2MTZjNjgzMzc5NGE0YjY4NzEyZDc1NDM3NjYyNjM3NjZiNmM1ZjJkMzQ2OTU3NGYyZDM0MzM3MjYxNDMzNDU5NmQ1MzY4NzE1MTQxNWY0YzRjNTg0ODU3NDE2ZTMzNmQ1ODQ1Mzg1MDRjNjU3YTQ1NTIzMzcwNTM3MDU1NDkzODcyNzI0NjUzNTIzOTY3NWE1MDRiNmE0NTQ3NGE1Nzc3NTY2YzU4NDQ3YTM5Mzk1YTUyNDg1YTcxN2EzNjRlNjYzNDQ4NjE0ZDU1NzE2MjYxNGI2ZTU4NDY2NDQ3NzI1NTYzNmY2YzY3NjQ2ZTM0NjI3NzQ0NjY2ODQ4Mzc2NTUzNDc3MTc2NmIzNzRiMzM0YzY4NGYzNzcyMzU2YjczNTk1MzdhMmQ3MDRjNzYzMDQ2NTA1YTQ0Nzg3MDUzMmQ1ZjY4NmQ1ZjM2NDMzODQzNDY2ODM4NTM0NTUxNjM1YTY1MzM0MTMxNDE2ZTcxNzk2OTZkNTc1NzQ5NDMzNDRiNjYzMTYzNDU2NTc2NWEzNTQ4NDQ2YzQ5NGMzMzQ4NmYzMzUwNGU3OTU1NzE2MTU5NzIzNDM0NDYzMzRmNTU1ODZiNjY0ODc5NmIzOTQxNDEzNzQ0NDgzMDVmNTUzMTQ2NGM0MTc3NTI2ZDc1NjQ3MjM4NzgzNzUwNDQ2YzY3N2E1ODMzNWEzNDY2Mzg2NjMxNTY2ZjU3NzU2OTQ0NmE2NjczNGE1ZjY3NTQ0YzYyNzE3OTRhNjkzNTUzNjc1ZjQzNTM0MjRmMzA0NjYyN2E2NTc1NTk1ODc4NmQzMjY5NzY0ZjMyNjY2MjVhNDk3NTcwNjI2ZjU1Njg2YTM0NDU2OTZmNGU0NzMzNmU2YTU3Mzc1NjZjNzQ2ZjRiNTY0ZDRjNDYzMjZkNmI1MDYzNzc2ODYzMzkzNTc0NmU2NjM4Njg2NjRiNTc1NzQ3NDg1ZjQyNDQ2MTMyNmM2MzU1NGQ3NzRmNGE3NTc1NjE2NTQ1NDI0MjczNjc3NzM5NTQ0YjQxNGU3Njc4NzQ0MjRlMzE3NDRhNmQ0YTM4MzM3NDZlN2E3MDZjNDgzNTZlNzAyZDcyNDk0NTc1NDI1ODZmNzQ2NzcwNDI3Mjc2Mzk1NTc4NDI1NzVhMzk1ODY3Njc0NDVmMzU0YzUxNzQ2MjQ1NjU1MjMzNDY2NDZkNTc1MzM0NjQzMjM1MzM0Nzc1NzUzMjUyN2E3ODMxNjI2MzMxNTU2MTZiNDQ2NzRkNjI0NTRiNzM0ZjZiMzI0ZTM4MmQ3NTQ2MzQ2ZjQ3NjI0ZTU3NjU1YTcxNGE0NDc3NmI3OTZiNDU2NTRlMzg2NjU0NTA0MjRhNDk3MjQ1NDQ2ZTU1NmU1NjYyNDkzNjRiNmM2ZjY4NGQ0NjZjNmE1OTQ0NDU1NDMwNzYzMzc0NTQ3NTc0NzI3ODQ2NmM0NzRkNjgzOTRmMzA0ODRlMzA1NjZjNDQ3NTc3NGQ0NjM2N2E1NDczNzMzNjRiNTI3NTY1Njc1NjRlNGU2YjVmNjk2ZDZlNDgzOTYyN2E0ZjRmNDczMzZhNGY0YjZlMzU0ZjM2NDM0YjUyNTM1ZjdhNDk3NTU2NGE2NzM0NTYzNjRkNGY0YjRkMzM2ZDM0MzI1NjY1MzE2OTVmNjM1NTMyNjY2ZjM0NDE2YjM1NzA0NDc5NWE0ZjQ0Mzg1OTU5NDQ3NTM0N2E3YTc0NjE0YjVhMzY3Nzc3NWY0NDM3Mzk2MzY2NTA0MTZjNDkzMzQ2NTk1ZjMxNzY0ODRiNWEzNjQxNzA1NjQ2NTc1MzZlNGIzMTZlNmYyZDYyNzA2Yjc0NGQzODY5Nzg3MDM5NWY1MTMwNGY3NjY3NDU3ODM2NDI0ZDM3NTI3MjY2NmI0ZDM3NmQ0ODYxNmE2MTYzNmI1NDc3MzQ2NjQyNGMzOTRlNDc1NjMwNzE0ZDZiNDk2ZDU5NmQ2YzMwMmQ1ODQ3NmQzODY1NDEzNjU3NzMzMzU5NDk0ODVhNDc1ZjM1NzM2ODQyNGY0YTM3MzY0ZDc4NTczNDQ5NmQ1ZjRiN2EyZDQ4Nzg0NjcxNDE3YTYzNDQ3MjQ3NTM0MTQ5NTE2NTc0NjU0OTczNzg3YTU2MzQ2YjRlN2E2NTQ3NDYzMDMyMzY1NTQ4Mzg2ZDMwMmQ3OTQxNjI2YzVmMzA0OTY5NzM0YjQ4Nzg2NzM0NTM2ZjMzNTM3MzZmNmY2YzMyMzg1MjY4NTY1NTMzNzg1NTQ4MzgzOTU0Nzg0YTY0NTM2ODZjNjk2Mzc4NDI0ODVmNjQ0YzYxNGQ2ZTc5NzM0YjZlNzk2YTc5MzU2MjM0NTQzMDcwNjU3MzMyNzU2NzU4NDQ2ZDMxNzg1YTMyNjQ3NjZiNDc2NTZlNmM0YjQ0NzYzMDZkNTA2YzQ0NTM3NzMyNzA2MzUxNDc2OTU3Nzc1MTM0NTY2MzUyNTM0OTZjNjM1MzRkNWE2YTU3NTM1NDZjNTU3YTY2Njc0ODRkNTI2OTQ1NzM1NjU4NTU1ZjYzNTU0MzRhNGI1ZjMzNTQ0ODU2NmE2YjZmNjc2NjM4NTU2MzMxNGY3NTc0NDU2NzJkNzk1YTZlNjk2MTRmNGUzMDc0NTYzMTQ3NzkzMjQ0Nzg0NjMzMmQzMzVhMzQ3NzM1MzU3NTM1NTk1ZjQ1NmM1ODYyNTY3OTY3NGU2MzVhNjIzNTU5MzI3NTRkNGY0NjMwNjU1NjcyNDQ3NDZkNTg0YjU2NjU3MzUzNGMzMTM1NzY2NTc4N2E0MjRmNDI2MzZjMzA3NzRjNTM3YTZlMzI2YzQ0NmMzMTc3NjE0NzMxNDI0NTRmNGQ3NTRiMmQ0NDQ5NGI2ZjczNjk0YTM3NTM0NjQ3NWE0OTRjNzg2ZTY1NGM2NjQ5MzIyZDVmNDI0NTY0NmY2MjMzNTkzOTM1NGUyZDQ0NDM1NDczNzU3MjM0NmQ3MTY3MzE1ZjU2MzI1NDQ1NzU1YTUwNjQ1MzQ4NmQ2MjU1NDc3MTM5MzU1MTJkNWE0NTM1NmI0MTc3NmY2MTYzMzQ1NzM3NmE3NjQ2NjM2MTUxMzkzMTUxNzk0NzMzNTI1ODUwNzE2ODc2NTUzOTU5NjY3OTc4NjI1OTM4NzkyZDc3NGY2ZDc4NDI3NzQ3Mzk2ODU1MmQzNDc3NTI3NDZhMmQ1NzRiMzEyZDZlMzIzNzc3NmI1NzQyMzQ0MzZjNmE0ZTZjNDg1MjM2NGY0NTY2MzE0NzRkNDc1YTQyMzY3OTVhNDM2OTYyNDY0OTMyNmY1NjQ2NTY2YTM3NjI0ODVhNTI0ZTczNzY0Mjc4MzEzNjM4NDg2MzNkIiwiZXhwIjoxNzg1MjY5NTE3fQ.DKuz8Y1Wsypn_pH90PBLuBjaB-T09WQ4xOPK27qZ8BDbOCqNBVEOs3MmfFWqxOp6RL0bXdzbT2EK3tv4TuJHTfqtTn7fEKrz35YFHN6qKZrc3IymwApIKWXn9YaKcXcRr3FeM1qoFCJtS8_cE5uyge3Z5B0Ndn26bpOEPmp0hnQ"

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
    "AWAITING_STAR_COURSE": "star_change"
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
        await bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте снова.')
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
            total_sum = (amount * star_course)
            if not cur.execute(f'SELECT * FROM Invoices WHERE user_id = {call.from_user.id}').fetchall():
                invoice = await cb.create_invoice(amount=total_sum, currency_type="fiat", fiat="RUB", description=f'Оплата {amount} звезд',
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
                invoice = await cb.create_invoice(amount=total_sum, currency_type='fiat', fiat='RUB' , description=f'Оплата {amount} звезд',
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
        await bot.delete_message(call.message.chat.id, call.message.id)
        await bot.send_photo(call.message.chat.id, buying_picture, caption=f'<b>Количество звезд:</b> <code>{amount}</code>\n<b>Сумма к оплате:</b> <code>{total_sum} {call.data}</code>\n<i>После оплаты нажмите кнопку "Я оплатил"</i>', reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        await bot.send_message(call.message.chat.id ,f'Ошибка: {e}')

@bot.callback_query_handler(func=lambda call: call.data == 'try_to_buy')
async def try_to_buy(call: types.CallbackQuery):
    try:
        invoice = cur.execute(f'''SELECT invoice_id, sum FROM Invoices WHERE user_id = "{call.from_user.id}"''').fetchone()
        invoice_id = await cb.get_invoice(int(invoice[0]))
        if invoice_id.status:
            if invoice_id.status == 'paid':
                quantity = cur.execute(f'SELECT amount FROM Clients WHERE user_id = "{call.from_user.id}"').fetchone()[0]
                await bot.answer_callback_query(call.id, 'Оплата прошла успешно')
                await bot.send_message(call.message.chat.id, '<b>🛒Оплата прошла успешно\nЗвезды будут зачислены на баланс в течение 2-10 минут</b>\n<tg-spoiler>Если звезды не пришли в течение часа, пожалуйста обратитесь в поддержку</tg-spoiler>', parse_mode="HTML")
                response = Fragment.buy_stars(call.from_user.username, int(quantity), show_sender=False, tkn=fragment_token)
                if response:
                    cur.execute(f'''UPDATE Clients
                                    SET success_purchases = success_purchases + 1
                                    WHERE user_id = {call.from_user.id}
                                    ''')
                    cur.execute(f'INSERT INTO Purchases(user_id, amount) VALUES({call.from_user.id}, {invoice[1]})')
                    cur.execute(f'DELETE FROM Invoices WHERE user_id = {call.from_user.id}')
                    con.commit()
            elif invoice_id.status == 'active':
                await bot.answer_callback_query(call.id, 'Оплата не прошла, попробуйте еще раз')
            elif invoice_id.status == 'expired':
                await bot.answer_callback_query(call.id, 'Срок оплаты истек, попробуйте снова')
                cur.execute(f'DELETE FROM Invoices WHERE user_id = {call.from_user.id}')
                con.commit()
        else:
            await bot.send_message(call.message.chat.id, 'Нет активных чеков для оплаты')
    except Exception as e:
        await bot.send_message(call.message.chat.id, f'Ошибка: {e}')



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


#основная функция для запуска бота
async def main():
    await bot.infinity_polling()

if __name__ == '__main__':
    run(main())
