import mysql.connector
import config
from mysql.connector import errorcode


pool_name = "line_pool"
# MySQL Database config
dbconfig = {
    "host": config.DB_HOST,
    "user": config.DB_USER,
    "password": config.DB_PASSWORD,
    "database": "line",
}

# Create MySQL pooling
mydb = mysql.connector.connect(
    pool_name=pool_name,
    pool_size=config.DB_POOL_SIZE,
    auth_plugin="mysql_native_password",
    **dbconfig,
)
mydb.close()


class db:
    def checkAllData(self, sql, val=()):
        # return data type is dictionary
        mydb = mysql.connector.connect(pool_name=pool_name)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()  # fetch all data
        mycursor.close()
        mydb.close()
        return myresult

    def checkOneData(self, sql, val):
        # return data type is dictionary
        mydb = mysql.connector.connect(pool_name=pool_name)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()  # fetch one data
        mycursor.close()
        mydb.close()
        return myresult

    def writeData(self, sql, val):
        try:
            mydb = mysql.connector.connect(pool_name=pool_name)
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            last_row_id = mycursor.lastrowid
            mycursor.close()
            mydb.close()
            return last_row_id
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            return None
