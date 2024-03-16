from src.db.sqlite3 import Sqlite3

ins = Sqlite3()
ins.cursor.execute('select * from stock_code')

for row in ins.cursor:
    print(row)

