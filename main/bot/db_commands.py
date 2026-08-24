import sqlite3

con = sqlite3.connect('StarBotClient.db')
cur = con.cursor()

cur.execute(f'INSERT INTO Exchange_rate(TON, USDT, STAR_COURSE) VALUES(250, 80, 1.4)')



con.commit()
con.close()