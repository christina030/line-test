import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a little-soul').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# 創造表格的SQL指令 = '''CREATE TABLE account(
#    user_id serial PRIMARY KEY,
#    username VARCHAR (50) UNIQUE NOT NULL,
#    password VARCHAR (50) NOT NULL,
#    email VARCHAR (355) UNIQUE NOT NULL,
#    created_on TIMESTAMP NOT NULL,
#    last_login TIMESTAMP
# );'''

# cursor.execute(創造表格的SQL指令)
# conn.commit()

cursor.close()
conn.close()
