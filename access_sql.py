import mysql.connector
import pandas
from sqlalchemy import create_engine

def fetch_table_data(table_name):
    # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object.
    cnx = mysql.connector.connect(
        host="192.46.216.64",
        user="otto",
        passwd="123456",
        database="mainTweetsV1"
    )

    cursor = cnx.cursor()
    cursor.execute('select * from ' + table_name)

    header = [row[0] for row in cursor.description]

    rows = cursor.fetchall()

    # Closing connection
    cnx.close()

    return header, rows

def export(table_name):
    header, rows = fetch_table_data(table_name)

    # Create csv file
    f = open(table_name + '.csv', 'w')

    # Write header
    f.write(','.join(header) + '\n')

    for row in rows:
        f.write(','.join(str(r) for r in row) + '\n')

    f.close()
    print(str(len(rows)) + ' rows written successfully to ' + f.name)

def uploadToSQL(df):

    df['created_at'] = pandas.to_datetime(df.created_at)
    df['account_created'] = pandas.to_datetime(df.account_created)
    engine = create_engine("mysql+pymysql://{user}:{pw}@192.46.216.64/{db}"  
                      .format(user="otto", pw="123456", 
                      db="mainTweetsV1"))

    df.to_sql('tweets2', con = engine, if_exists = 'append',index=False, chunksize=10000)