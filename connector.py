import mysql.connector
import os

def connection():
    try:
        cnx = mysql.connector.connect(
            host='xrmain.cbznpx7q4pii.us-east-2.rds.amazonaws.com',
            user='admin',
            password='helloworld1!',
            db='test_db',
        )
        cursor = cnx.cursor()
        return cursor, cnx
    except Exception as err:
        print('Error in db connection: '+str(e))
        return 0,0