import os
import psycopg2
import re
# import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
# # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a little-soul').read()[:-1]

# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# cursor = conn.cursor()

# cursor.close()
# conn.close()

def table_exists(cursor, table_name):
    sql = 'SELECT ' + table_name + """ FROM information_schema.tables
           WHERE table_schema = 'public'"""
    # for table in cursor.fetchall():
    #     print(table)
    # sql = 'SHOW TABLES;'
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return True
    else:
        return False
    # return cursor.fetchone() is not None

def create_tables():    
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

def add_row(table_name, col_names, values):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
  
    if not table_exists(cursor, 'users'):
        cmd = '''CREATE TABLE users(
           user_id VARCHAR (50) NOT NULL,
           done_date DATE NOT NULL
        );'''
        cursor.execute(cmd)
        conn.commit()

    cursor.close()
    conn.close()
    return
