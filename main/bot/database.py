import sqlite3

con = sqlite3.connect('StarBotClient.db')
cur = con.cursor()

#Создание БД
cur.execute('''CREATE TABLE IF NOT EXISTS Clients(
                user_id TEXT PRIMARY KEY,
                state TEXT,
                amount INTEGER,
                balance INTEGER DEFAULT 0,
                create_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                success_purchases INTEGER DEFAULT 0,
                chat_id INTEGER
                )
                ''')

cur.execute('''CREATE TABLE IF NOT EXISTS Promo(
                promo TEXT PRIMARY KEY,
                amount_promo INTEGER NOT NULL,
                max_uses INTEGER NOT NULL,
                uses_now INTEGER NOT NULL DEFAULT 0
                )
                ''')

cur.execute('''CREATE TABLE IF NOT EXISTS used_promo(
                promo TEXT NOT NULL,
                user_id INTEGER NOT NULL
                )
                ''')


cur.execute('''CREATE TABLE IF NOT EXISTS Invoices(
                invoice_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                status TEXT,
                sum INTEGER,
                created_time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                ''')

cur.execute(f'''CREATE TABLE IF NOT EXISTS Admin(
                user_id INTEGER PRIMARY KEY
                )
                ''')

cur.execute(f'''CREATE TABLE IF NOT EXISTS Purchases(
                user_id INTEGER,
                amount INTEGER NOT NULL,
                time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                ''')

cur.execute(f'''CREATE TABLE IF NOT EXISTS Exchange_rate(
                TON INTEGER NOT NULL,
                USDT INTEGER NOT NULL,
                STAR_COURSE REAL NOT NULL
                )
                ''')

con.commit()
con.close()
