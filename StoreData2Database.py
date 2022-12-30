import json
import os
import mysql.connector
from mysql.connector import errorcode




def image_url(urlstr):
    imgurl=urlstr.split("https://")# split the string in the file
    imgurl.remove("")# remove empty string in the list
    imgurl=["https://" +item for item in imgurl]
    # print(imgurl)
    return imgurl


abs_path=os.path.dirname(os.path.abspath(__file__))
relative_path="data/taipei-attractions.json"
full_path=os.path.join(abs_path, relative_path)
f=open(full_path, 'r')

data=json.load(f)
f.close()
data=data["result"]["results"]
# cols=data[0].keys()
# print(cols)
# print(type(cols))
# print(len(cols))
# vals=data.values()
# sql="insert into %s(%s) values(%s)"

# Define tables
TABLES={}
TABLES['attractions'] = (
    "CREATE TABLE `attractions` ("
    "  `rate` int not null,"
    "`transport` varchar(1000) not null,"
    "`name` varchar(255) not null,"
    "`date` varchar(20) not null,"
    "`lng` float not null,"
    "`REF_WP` int not null,"
    "`avBegin` varchar(20) not null,"
    "`langinfo` int not null,"
    "`mrt` varchar(40) default 'NONE',"
    "`SERIAL_NO` bigint not null,"
    "`RowNumber` int not null,"
    "`category` varchar(255) not null,"
    "`MEMO_TIME` varchar(2000) default 'NONE',"
    "`POI` varchar(4) not null,"
    "`idpt` varchar(255) not null,"
    "`lat` float not null,"
    "`description` varchar(2000) not null,"
    " `id` int(100) NOT NULL,"
    "`avEnd` varchar(20) not null,"
    "`address` varchar(100) not null,"
    "  PRIMARY KEY (`id`) "
    ") ENGINE=InnoDB")

TABLES['imgURL'] = (
    "CREATE TABLE `imgURL` ("
    " `url_id` int not null auto_increment,"
    "  `id` int(100) not null, "
    "  `images` varchar(2000) NOT NULL,"
    "  PRIMARY KEY (`url_id`),"
    "  CONSTRAINT `imgURL_ibfk_1` FOREIGN KEY (`id`) REFERENCES `attractions` (`id`) ON DELETE CASCADE "
    ") ENGINE=InnoDB")

TABLES['member']=(
    "CREATE TABLE `member` ("
    "`member_id` bigint not null auto_increment primary key,"
    "`username` varchar(255) not null,"
    "`email` varchar(320) not null,"
    "`password` varchar(255) not null"
    ") ENGINE=InnoDB")

TABLES['booking']=(
    "CREATE TABLE `booking` ("
    "`booking_id` bigint not null auto_increment primary key,"
    "`member_id` bigint not null,"
    "`attraction_id` int(100) not null,"
    "`date` date not null,"
    "`time` varchar(10) not null,"
    "`price` int not null default 2000,"
    "`confirmation` boolean not null default FALSE,"
    "foreign key(`member_id`) references `member` (`member_id`) on delete cascade on update cascade,"
    "foreign key(`attraction_id`) references `attractions` (`id`) on delete cascade on update cascade"
    ") ENGINE=InnoDB")

TABLES['orders']=(
    "CREATE TABLE `orders` ("
    "`order_id` bigint not null auto_increment primary key,"
    "`booking_id` bigint not null,"
    "`order_num` varchar(20) not null,"
    "`transaction_status` int(10) not null,"
    "`transaction_msg` varchar(300) default null,"
    "`rec_trade_id` varchar(20) default null,"
    "`bank_transaction_id` varchar(40) not null,"
    "`bank_result_code` varchar(20) not null,"
    "`bank_result_msg` varchar(300) default null,"
    "`card_last_four` varchar(4) default null,"
    "`amount` bigint not null,"
    "`currency` varchar(3) not null,"
    "`phone` varchar(10) not null,"
    "foreign key(`booking_id`) references `booking` (`booking_id`) on delete cascade on update cascade"
    ") ENGINE=InnoDB")

TABLES["userPic"]=(
    "CREATE TABLE `userPic` ("
    "`pic_id` bigint not null auto_increment primary key,"
    "`member_id` bigint not null unique,"
    "`pic_path` varchar(255) not null,"
    "foreign key(`member_id`) references `member` (`member_id`) on delete cascade on update cascade"
    ") ENGINE=InnoDB")

# Connect to database
DB_NAME="TaipeiDayTrip"
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",
)

cursor=mydb.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        mydb.database = DB_NAME
    else:
        print(err)
        exit(1)

# Create tables
for table_name in TABLES:
    table_description = TABLES[table_name]
    # print(table_description)
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()

# Insert Data
add_attractions=("INSERT INTO attractions "
              "(rate, transport, name, date, lng, REF_WP, avBegin, langinfo, mrt, SERIAL_NO, RowNumber, category, MEMO_TIME, POI, idpt, lat, description, id, avEnd, address) "
              "VALUES (%(rate)s, %(direction)s, %(name)s, %(date)s, %(longitude)s, %(REF_WP)s, %(avBegin)s, %(langinfo)s, %(MRT)s, %(SERIAL_NO)s, %(RowNumber)s, %(CAT)s, %(MEMO_TIME)s, %(POI)s, %(idpt)s, %(latitude)s, %(description)s, %(_id)s, %(avEnd)s, %(address)s)")

add_imgURL=("INSERT INTO imgURL"
              "(id, images) "
              "VALUES (%(_id)s, %(file)s)")

cursor = mydb.cursor()


for item in data:
    # print(item.keys())
    # print(item["_id"])
    cursor.execute(add_attractions, item)
    mydb.commit()
    imgurl=image_url(item["file"])
    for url in imgurl:
        cursor.execute(add_imgURL, {"_id": item["_id"], "file":url})
        mydb.commit()
        

cursor.close()
mydb.close()


