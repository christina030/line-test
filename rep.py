import os
import psycopg2
# import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
# DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a little-soul').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.close()
conn.close()

def table_exists(cursor, table_name):
    cursor = conn.cursor()
    sql = "SHOW TABLES LIKE '%s'" % table_name
    cursor.execute(sql)
    return cursor.fetchone() is not None

def create_tables():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
  
    if not table_exists(cursor, 'users'):
        cmd = '''CREATE TABLE users(
           user_id VARCHAR (50) NOT NULL,
           done_date DATE NOT NULL
        );'''
        cursor.execute(cmd)
        conn.commit()
    
    if not table_exists(cursor, 'actions'):
        cmd = '''CREATE TABLE actions(
           user_id VARCHAR (50) NOT NULL,
           done_date DATE NOT NULL
        );'''
        cursor.execute(cmd)
        conn.commit()
    
    if not table_exists(cursor, 'scores'):
        cmd = '''CREATE TABLE scores(
           user_id VARCHAR (50) NOT NULL,
           score1 SMALLINT NOT NULL,
           score2 SMALLINT,
           score3 SMALLINT,
           score4 SMALLINT,
           score5 SMALLINT
        );'''
        cursor.execute(cmd)
        conn.commit()
    
    if not table_exists(cursor, 'msgs'):
        cmd = '''CREATE TABLE msgs(
           user_id VARCHAR (50) NOT NULL,
           token VARCHAR (50) NOT NULL,
           mood SMALLINT NOT NULL
        );'''
        cursor.execute(cmd)
        conn.commit()
    
    cursor.close()
    conn.close()
