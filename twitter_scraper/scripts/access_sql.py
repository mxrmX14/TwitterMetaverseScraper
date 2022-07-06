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
    database = str(config['sql']['database'])
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
    host, user, passwd, database = readConfig()
    sql_table_name = "tweets"
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"  
                      .format(user=user, pw=passwd, 
                      db=database, host=host))

    data = pandas.read_sql_table(sql_table_name, con=engine)
    filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'tables/'+table_name+'.csv'))
    data.to_csv(filepath, mode='a', header=True, index=False)
    print(data.head)



