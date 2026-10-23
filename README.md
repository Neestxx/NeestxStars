<div align="center">

# NeestxStars

**Telegram-магазин Stars с оплатой, промокодами и историей покупок.**

Telegram Stars storefront with payment integrations and administration tools.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)
![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-AsyncTeleBot-111827?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![aiosend](https://img.shields.io/badge/aiosend-Crypto_Pay-8250DF?style=flat-square)

[Возможности](#features) · [Технологии](#stack) · [Запуск](#setup) · [Структура](#structure)

</div>

---

**NeestxStars** — самостоятельно разработанный Telegram-бот для продажи Stars. В одном интерфейсе собраны выбор количества звёзд, платёжные сценарии, профиль покупателя и инструменты администратора.

Публичная версия содержит шаблонные реквизиты. Перед запуском требуется настроить платёжные сервисы, интеграцию покупки Stars и начальные данные.

<a id="features"></a>
## Возможности

| Для покупателя | Для администратора |
| :--- | :--- |
| Выбор количества Stars и подтверждение покупки | Создание промокодов и настройка лимита применений |
| Платёжные сценарии в рублях и криптовалюте | Настройка курсов TON, USDT и цены Stars |
| Личный кабинет, баланс и история покупок | Статистика и список активных покупателей |
| Использование промокодов | Рассылки, в том числе с изображениями |
| Обращение в поддержку | Добавление и удаление администраторов |

Бот также содержит проверку подписки на заданный Telegram-канал и сценарии отмены покупки.

<a id="stack"></a>
## Технологии

| Компонент | Решение |
| :--- | :--- |
| Telegram-интерфейс | Python · pyTelegramBotAPI / AsyncTeleBot |
| Хранение данных | SQLite · стандартный модуль sqlite3 |
| Криптовалютные платежи | aiosend / Crypto Pay |
| Рублёвые платежи | Модуль интеграции Apays |
| Покупка Stars | HTTP-интеграция через `api.fragment-api.com` |
| Запросы к внешним сервисам | requests |

> Модуль покупки Stars обращается к **стороннему API `fragment-api.com`**. Его доступность и требования к авторизации нужно проверять отдельно; это не прямой вызов Telegram Bot API.

<a id="setup"></a>
## Настройка и запуск

Для настройки рекомендуется **Python 3.12** и виртуальное окружение. В коде используются f-строки с синтаксисом Python 3.12. Потребуются Telegram-бот и собственные реквизиты выбранных платёжных сервисов.

### 1. Подготовьте окружение

```bash
git clone https://github.com/Neestxx/NeestxStars.git
cd NeestxStars
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

<details>
<summary><b>Активация окружения в Windows PowerShell</b></summary>

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

</details>

### 2. Настройте интеграции

В текущей версии параметры задаются непосредственно в исходных файлах — загрузка `.env` не реализована.

| Файл | Что настроить |
| :--- | :--- |
| [`main/bot/main.py`](main/bot/main.py) | Токен Telegram-бота, Crypto Pay, `fragment_token`, чат поддержки и канал для проверки подписки |
| [`main/bot/Apay.py`](main/bot/Apay.py) | Идентификатор клиента и секрет для создания и проверки платежей |
| [`main/bot/fragment_requests.py`](main/bot/fragment_requests.py) | Параметры авторизации и взаимодействия со сторонним API покупки Stars |
| [`main/bot/telegram_keyboards.py`](main/bot/telegram_keyboards.py) | Ссылки в кнопках и параметры интерфейса |
| [`main/bot/url.py`](main/bot/url.py) | Изображения и ссылка на правила сервиса |

<details>
<summary><b>Обязательная настройка Apay.py перед запуском</b></summary>

В двух словарях `params` оставлено выражение `"client_id": id клиента`. Это текстовая заглушка, которая вызывает синтаксическую ошибку Python.

Замените обе заглушки своим идентификатором в формате, предусмотренном платёжным сервисом, и настройте секрет и расчёт подписи. Пока это не сделано, импорт `Apay.py` и запуск бота невозможны.

Рабочие реквизиты храните локально и не включайте в публичные коммиты. Для развёртывания рекомендуется вынести их в переменные окружения с соответствующим изменением кода.

</details>

### 3. Создайте базу и начальные данные

Все последующие команды выполняются из `main/bot`, чтобы приложение использовало один и тот же файл SQLite:

```bash
cd main/bot
python database.py
```

Будет создан файл `StarBotClient.db` с таблицами пользователей, платежей, покупок, промокодов, администраторов и курсов.

Перед первым запуском:

1. В таблице `Exchange_rate` создайте **одну** строку с актуальными значениями `TON`, `USDT` и `STAR_COURSE`.
2. В таблицу `Admin` добавьте свой числовой Telegram user ID в поле `user_id`.

В [`db_commands.py`](main/bot/db_commands.py) есть пример заполнения курсов. Сначала замените демонстрационные значения своими. Скрипт каждый раз добавляет новую строку, поэтому его не следует запускать повторно без проверки содержимого таблицы.

### 4. Запустите бота

После завершения настройки, оставаясь в каталоге `main/bot`:

```bash
python main.py
```

Проверьте начало диалога, подписку на канал, профиль, применение промокода и полный сценарий покупки. Интеграции с реальными платежами и выдачей Stars требуют отдельной проверки на ваших реквизитах.

<a id="structure"></a>
## Структура проекта

```text
NeestxStars/
├── main/
│   └── bot/
│       ├── main.py                # Обработчики и запуск бота
│       ├── database.py            # Создание таблиц SQLite
│       ├── db_commands.py         # Пример заполнения курсов
│       ├── fragment_requests.py   # Авторизация и покупка Stars через API
│       ├── Apay.py                # Создание и проверка рублёвых платежей
│       ├── telegram_keyboards.py  # Клавиатуры и кнопки
│       └── url.py                 # Изображения и ссылки
└── requirements.txt
```

<details>
<summary><b>Назначение проекта и ответственность</b></summary>

Проект опубликован в образовательных и исследовательских целях. Пользователь самостоятельно отвечает за использование кода, соблюдение применимого законодательства и требований сторонних сервисов. Автор не поддерживает противоправное использование проекта.

</details>

---

<div align="center">

**Разработчик — [Neestxx](https://github.com/Neestxx)**

Предложения и сообщения об ошибках — через [Issues](https://github.com/Neestxx/NeestxStars/issues).

Значительные изменения лучше предварительно обсудить; pull request'ы приветствуются.

</div>
