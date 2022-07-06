from fileinput import filename
import mysql.connector
import pandas
from configparser import RawConfigParser
import os
from sqlalchemy import create_engine

def readConfig():
    filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'authentication/'+'config.ini'))
    config = RawConfigParser()
    config.read(filepath)
    host = str(config['sql']['host'])
    user = str(config['sql']['user'])
    passwd = str(config['sql']['passwd'])
    database = str(config['sql'][database])
    return host, user, passwd, database

def fetch_table_data(sql_table_name):

    host, user, passwd, database = readConfig()

    # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object. 
    cnx = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )

    cursor = cnx.cursor()
    cursor.execute('select * from ' + sql_table_name)

    header = [row[0] for row in cursor.description]

    rows = cursor.fetchall()

    # Closing connection
    cnx.close()

    return header, rows

def export(table_name):
    sql_table_name = "tweets"
    header, rows = fetch_table_data(sql_table_name)

    # Create csv file
    filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'tables/'+table_name+'.csv'))
    f = open(filepath, 'w')

    # Write header
    f.write(','.join(header) + '\n')

    for row in rows:
        f.write(','.join(str(r) for r in row) + '\n')

    f.close()
    print(str(len(rows)) + ' rows written successfully to ' + f.name)


# def uploadToSQL(df):

#     df['created_at'] = pandas.to_datetime(df.created_at)
#     df['account_created'] = pandas.to_datetime(df.account_created)
#     engine = create_engine("mysql+pymysql://{user}:{pw}@{db}"  
#                       .format(user="", pw="", 
#                       db=""))

#     df.to_sql('tweets', con = engine, if_exists = 'append',index=False, chunksize=10000)