import mysql.connector
import config
from mysql.connector import errorcode


# MySQL Database config
dbconfig = {
    "host": config.DB_HOST,
    "user": config.DB_USER,
    "password": config.DB_PASSWORD,
    "database": config.DB_DB
}


# Create MySQL pooling
mydb = mysql.connector.connect(
    pool_name=config.DB_POOL_NAME,
    pool_size=config.DB_POOL_SIZE,
    **dbconfig
)
mydb.close()


class db:

    def checkAllData(sql, val=()):
        # return data type is dictionary
        mydb = mysql.connector.connect(pool_name=config.DB_POOL_NAME)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()  # fetch all data
        mycursor.close()
        mydb.close()
        return myresult

    def checkOneData(sql, val=()):
        # return data type is dictionary
        mydb = mysql.connector.connect(pool_name=config.DB_POOL_NAME)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()  # fetch one data
        mycursor.close()
        mydb.close()
        return myresult

    def writeData(sql, val):
        try:
            mydb = mysql.connector.connect(pool_name=config.DB_POOL_NAME)
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()
            return True
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            return False

    def search_image_by_id(id):
        sql = "select images from imgURL where id= %s and (lower(images) like '%jpg' or lower(images) like '%jpeg' or lower(images) like '%png')"
        val = (id,)

        result = db.checkAllData(sql, val)
        return result

    def search_by_keyword(keyword, page, NumInOnePage):
        ambig_keyword = '%' + keyword + '%'
        sql = "select id, name, category, description, address, transport, mrt, lat, lng from attractions "\
            "where (category= %s or name like %s) "\
            "order by id asc "\
            "limit %s, %s"
        val = (keyword, ambig_keyword, page * NumInOnePage, NumInOnePage + 1,)

        result = db.checkAllData(sql, val)
        return result

    def search_by_page(page, NumInOnePage):
        sql = "select id, name, category, description, address, transport, mrt, lat, lng from attractions order by id asc limit %s, %s "
        val = (page * NumInOnePage, NumInOnePage + 1,)

        result = db.checkAllData(sql, val)
        return result

    def search_by_id(id):
        sql = "select id, name, category, description, address, transport, mrt, lat, lng from attractions where id = %s"
        val = (id,)

        result = db.checkAllData(sql, val)
        return result

    def search_catogories():
        sql = "select distinct category from attractions"
        result = db.checkAllData(sql)
        return result

    def search_member_by_email(email):
        sql = "select * from member where email=%s"
        val = (email,)

        result = db.checkOneData(sql, val)
        return result

    def register(username, email, psw):
        sql = "insert into member (username, email, password) values (%s, %s, %s)"
        val = (username, email, psw,)

        result = db.writeData(sql, val)
        return result

    def check_booking(id):
        sql = "select attractions.id, attractions.name, attractions.address, imgURL.images, booking.date, booking.time, booking.price, booking.booking_id "\
            "from booking "\
            "inner join attractions "\
            "on attractions.id = booking.attraction_id "\
            "inner join member "\
            "on member.member_id = booking.member_id "\
            "inner join imgURL "\
            "on imgURL.id = attractions.id "\
            "where member.member_id= %s and booking.confirmation=False "\
            "limit 1"
        val = (id,)
        result = db.checkAllData(sql, val)
        return result

    def build_booking(member_id, attraction_id, date, time, price):
        sql = "insert into booking (member_id, attraction_id, date, time, price) "\
            "values (%s, %s, %s, %s, %s)"
        val = (member_id, attraction_id, date, time, price,)
        result = db.writeData(sql, val)
        return result

    def update_booking(member_id, attraction_id, date, time, price):
        sql = "update booking set attraction_id=%s, date=%s, time=%s, price=%s "\
            "where member_id =%s"
        val = (attraction_id, date, time, price, member_id,)
        result = db.writeData(sql, val)
        return result

    def confirm_booking(user_id):
        sql = "update booking set confirmation = True where member_id=%s"
        val = (user_id,)
        result = db.writeData(sql, val)
        return result

    def delete_booking(user_id):
        sql = "delete from booking where member_id= %s and confirmation = False"
        val = (user_id,)
        result = db.writeData(sql, val)
        return result

    def record_order(payment_response, booking_id, phone):
        sql = "insert into orders (booking_id, order_num, "\
            "transaction_status, transaction_msg, rec_trade_id, "\
            "bank_transaction_id, bank_result_code, bank_result_msg, "\
            "card_last_four, amount, currency, phone) "\
            "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            booking_id,
            payment_response["order_number"],
            payment_response["status"],
            payment_response["msg"],
            payment_response["rec_trade_id"],
            payment_response["bank_transaction_id"],
            payment_response["bank_result_code"],
            payment_response["bank_result_msg"],
            payment_response["card_info"]["last_four"],
            payment_response["amount"],
            payment_response["currency"],
            phone)
        result = db.writeData(sql, val)
        return result

    def get_order_by_orderNum(orderNum):
        sql = "select orders.order_num, booking.price, attractions.id, attractions.name, attractions.address, imgURL.images, booking.date, booking.time, member.username, member.email, orders.phone, orders.transaction_status "\
            "from orders "\
            "inner join booking "\
            "on orders.booking_id= booking.booking_id "\
            "inner join attractions "\
            "on booking.attraction_id=attractions.id "\
            "inner join imgURL "\
            "on imgURL.id = attractions.id "\
            "inner join member "\
            "on member.member_id=booking.member_id "\
            "where orders.order_num=%s "\
            "limit 1"
        val = (orderNum,)
        result = db.checkAllData(sql, val)
        return result

    def get_member_order(member_id):
        sql = "select DATE_FORMAT(booking.date, '%Y-%m-%d') as date, booking.time, "\
            "booking.price, booking.booking_id, attractions.id, attractions.name, "\
            "attractions.address, imgURL.images, orders.order_num "\
            "from booking "\
            "inner join orders "\
            "on orders.booking_id = booking.booking_id "\
            "inner join attractions "\
            "on booking.attraction_id=attractions.id "\
            "inner join imgURL "\
            "on imgURL.url_id=(select url_id from imgURL where id=attractions.id limit 1) "\
            "where member_id=%s"
        val = (member_id,)
        result = db.checkAllData(sql, val)
        return result

    def delete_order(order_num, member_id):
        sql = "delete booking, orders from orders inner join booking on booking.booking_id=orders.booking_id and booking.member_id=%s where orders.order_num=%s"
        val = (member_id, order_num,)
        result = db.writeData(sql, val)
        return result

    def get_refund_id(order_num):
        sql = "select rec_trade_id, amount from orders where order_num=%s"
        val = (order_num,)
        result = db.checkOneData(sql, val)
        result = result["rec_trade_id"]
        return result

    def update_member(member_id, username, email, password):
        if username:
            sql = "update member set username=%s where member_id=%s"
            val = (username, member_id,)
            result = db.writeData(sql, val)
            return result
        elif email:
            sql = "update member set email=%s where member_id=%s"
            val = (email, member_id,)
            result = db.writeData(sql, val)
            return result
        elif password:
            sql = "update member set password=%s where member_id=%s"
            val = (password, member_id,)
            result = db.writeData(sql, val)
            return result

    def uploadUserPic(member_id, file_path):
        if db.loadUserPic(member_id):
            sql = "update userPic set pic_path=%s where member_id=%s"
        else:
            sql = "insert into userPic (pic_path, member_id) values (%s, %s)"
        val = (file_path, member_id,)
        result = db.writeData(sql, val)
        return result

    def loadUserPic(member_id):
        sql = "select pic_path from userPic where member_id =%s"
        val = (member_id,)
        result = db.checkOneData(sql, val)
        return result
