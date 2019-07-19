from configparser import ConfigParser
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
import os

DB_CONFIG_FILE = os.path.dirname(__file__) + '/config.ini'


def config(filename=DB_CONFIG_FILE, section='pigLatin'):
    '''parse conf file '''
    '''create parser'''
    parser = ConfigParser()
    '''read the config'''
    parser.read(filename)
    '''get the section wanted'''
    db = {}
    if parser.has_section(section):
        print('Reading db config')
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]  # key value structure from file
    else:
        raise Exception('Section {0} is not found in {1} file'.format(section, filename))
    return db


def connect_to_rds():
    connection = None
    try:
        # read connection params
        params = config()
        # connect to postgre database
        print('Connecting to the PostgreSQL database')
        connection = psycopg2.connect(**params)
        # create a cursor
        cursor = connection.cursor()
        # execute a statement
        print('PostgreSQL Database Version:')
        cursor.execute('SELECT version()')
        # fetch the data
        db_version = cursor.fetchone()
        print(db_version)
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection closed")


def create_tables():
    commands = ("""      
        CREATE TABLE pigLatin (
          user_id SERIAL PRIMARY KEY,
          email VARCHAR(255) NOT NULL,
          word VARCHAR(255) NOT NULL,
          translation VARCHAR(255) NOT NULL

        )""", """CREATE TABLE users (
          user_id SERIAL PRIMARY KEY,
          username VARCHAR(255) NOT NULL,
          password_hash VARCHAR(255) NOT NULL         

        )""" )

    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def insert_rds(email, word, translation):
    sql_cmd = ('''INSERT into pigLatin(email,word,translation)
            VALUES (%s, %s, %s)''',)
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in sql_cmd:
            cursor.execute(command, (email, word, translation))
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def delete_record(email):
    sql_cmd = ('''Delete FROM pigLatin where email = %s''',)
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in sql_cmd:
            cursor.execute(command, (email,))
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def update_email_rds(old_email,new_email):
    sql_cmd = ("""Update pigLatin set email = %s where email = %s""",)
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in sql_cmd:
            cursor.execute(command, (new_email,old_email))
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def dropTable(tableName):
    sql_cmd = ("DROP TABLE IF EXISTS \"%s\";",)
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in sql_cmd:
            cursor.execute(command, (tableName,))
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def register(username,password):
    sql_cmd = ('''INSERT into users (username,password_hash)
            VALUES (%s, %s)''',)
    hashed_pw = generate_password_hash(password)
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in sql_cmd:
            cursor.execute(command, (username,hashed_pw))
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def validate_username_password(username,password):
    sql_cmd = ("Select password_hash from users where username = %s",)
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in sql_cmd:
            cursor.execute(command, (username,))

        hashed_password = cursor.fetchone()[0]
        if check_password_hash(hashed_password,password):
            verified = True
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
        return verified

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def check_username_exist(username):
    sql_cmd = ("Select username from users where username = %s",)
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        try:
            for command in sql_cmd:
                cursor.execute(command, (username,))
            user = cursor.fetchone()[0]
            exist = True
        except:
            exist = False
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
        return exist
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def fetchAllTranslations():
    sql_cmd = ("Select word,translation from pigLatin",)
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in sql_cmd:
            cursor.execute(command)
        results = cursor.fetchall()
        cursor.close()
        connection.commit()
        print('Commands executed successfully.')
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()




#AWS/FLASK/RDS/CRUD practice - API that returns pig latin translation of the input
#Data is written to RDS tables in AWS
#Elliott Arnold  7-19-19
#si3mshady
