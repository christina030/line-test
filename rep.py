import os
import psycopg2
import re
# import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
# # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a little-soul').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cmd = 'DROP TABLE users;'
cursor.execute(cmd)
cmd = 'DROP TABLE actions;'
cursor.execute(cmd)
cmd = 'DROP TABLE scores;'
cursor.execute(cmd)
cmd = 'DROP TABLE msgs;'
cursor.execute(cmd)
conn.commit()

cursor.close()
conn.close()

def table_exists(cursor, table_name):
    cmd = """SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'"""
    # for table in cursor.fetchall():
    #     print(table)
    # sql = 'SHOW TABLES;'
    cursor.execute(cmd)
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
           first_date DATE NOT NULL,
           first_time BOOL NOT NULL
        );'''
        cursor.execute(cmd)
        print('""" create users """')
    
    if not table_exists(cursor, 'actions'):
        cmd = '''CREATE TABLE actions(
           user_id VARCHAR (50) NOT NULL,
           done_date DATE
        );'''
        cursor.execute(cmd)
        print('""" create actions """')
    
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
        print('""" create scores """')
    
    if not table_exists(cursor, 'msgs'):
        cmd = '''CREATE TABLE msgs(
           user_id VARCHAR (50) NOT NULL,
           token VARCHAR (50) NOT NULL,
           mood SMALLINT NOT NULL
        );'''
        cursor.execute(cmd)
        print('""" create msgs """')
        
    conn.commit()
    
    cursor.close()
    conn.close()

def add_row(table_name, col_names, values):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
  
    # cmd = '''INSERT INTO table_name (column1, column2, column3, ...)
    #     VALUES (value1, value2, value3, ...);'''
    if isinstance(values, tuple):
        cmd = f'INSERT INTO {table_name} {col_names} VALUES {values};'
    elif isinstance(values, str):
        cmd = f'INSERT INTO {table_name} {col_names} VALUES (\'{values}\');'
    else:
        cmd = f'INSERT INTO {table_name} {col_names} VALUES ({values});'
    cursor.execute(cmd)
    conn.commit()
    print('""" add """', cmd)

    cursor.close()
    conn.close()

def modify_val(table_name, col_names, values, user_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
  
    # cmd = '''UPDATE table_name
    #     SET column1 = value1, column2 = value2, ...
    #     WHERE condition;'''
    print('""" modify """')
    for i in range(len(col_names)):
        if isinstance(values[i], str):
            cmd = f'UPDATE {table_name} SET {col_names[i]} = \'{values[i]}\' WHERE user_id = \'{user_id}\';'
        else:
            cmd = f'UPDATE {table_name} SET {col_names[i]} = {values[i]} WHERE user_id = \'{user_id}\';'
        cursor.execute(cmd)
        print(cmd)
    conn.commit()

    cursor.close()
    conn.close()

def read_data(table_name, col_names, user_id=None):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
  
    # cmd = '''SELECT column_names
    #     FROM table_name
    #     WHERE column_name IS NULL;'''
    # if user_id is None:
    #     cmd = 'SELECT ' + column_names + ' FROM ' + table_name + ';'
    # else:
    cmd = f'SELECT {col_names} FROM {table_name} WHERE user_id = \'{user_id}\';'
    cursor.execute(cmd)
    
    values = cursor.fetchone()

    cursor.close()
    conn.close()

    return values

def delete_row(table_name, user_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
  
    # cmd = '''DELETE FROM table_name WHERE condition;'''
    cmd = f'DELETE FROM {table_name} WHERE user_id = \'{user_id}\';'
    cursor.execute(cmd)
    conn.commit()
    print('""" delete """', cmd)
    
    cursor.close()
    conn.close()
