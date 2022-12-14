import mysql.connector
import config


# MySQL Database config
dbconfig={
	"host":config.DB_HOST,
	"user":config.DB_USER,
	"password":config.DB_PASSWORD,
	"database":config.DB_DB
}


# Create MySQL pooling
mydb=mysql.connector.connect(
	pool_name=config.DB_POOL_NAME,
	pool_size=config.DB_POOL_SIZE,
	**dbconfig
)
mydb.close()

class db:

    def checkAllData(sql, val=()):
        # return data type is dictionary
        mydb=mysql.connector.connect(pool_name=config.DB_POOL_NAME)
        mycursor=mydb.cursor(dictionary=True)
        mycursor.execute(sql, val)
        myresult=mycursor.fetchall() #fetch all data
        mycursor.close()
        mydb.close()
        return myresult

    def checkOneData(sql, val=()):
        # return data type is dictionary
        mydb=mysql.connector.connect(pool_name=config.DB_POOL_NAME)
        mycursor=mydb.cursor(dictionary=True)
        mycursor.execute(sql, val)
        myresult=mycursor.fetchone() # fetch one data
        mycursor.close()
        mydb.close()
        return myresult

    def writeData(sql, val):
        try:
            mydb=mysql.connector.connect(pool_name=config.DB_POOL_NAME)
            mycursor=mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()
            return True
        except:
            return False

    def search_image_by_id(id):
        sql="select images from imgURL where id= %s and (lower(images) like '%jpg' or lower(images) like '%jpeg' or lower(images) like '%png')"
        val=(id,)

        result=db.checkAllData(sql, val)
        return result

    def search_by_keyword(keyword, page, NumInOnePage):
        ambig_keyword='%'+keyword+'%'
        sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions "\
			"where (category= %s or name like %s) "\
			"order by id asc "\
			"limit %s, %s"
        val=(keyword, ambig_keyword, page*NumInOnePage, NumInOnePage+1,)
        
        result=db.checkAllData(sql, val)
        return result

    def search_by_page(page, NumInOnePage):
        sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions order by id asc limit %s, %s "
        val=(page*NumInOnePage, NumInOnePage+1,)

        result=db.checkAllData(sql, val)
        return result

    def search_by_id(id):
        sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions where id = %s"
        val=(id,)

        result=db.checkAllData(sql,val)
        return result

    def search_catogories():
        sql="select distinct category from attractions"
        result=db.checkAllData(sql)
        return result

    def search_member_by_email(email):
        sql="select * from member where email=%s"
        val=(email,)

        result=db.checkOneData(sql,val)
        return result

    def register(username, email, psw):
        sql="insert into member (username, email, password) values (%s, %s, %s)"
        val=(username, email, psw,)

        result=db.writeData(sql,val)
        return result

    def check_booking(id):
        sql = "select attractions.id, attractions.name, attractions.address, imgURL.images, booking.date, booking.time, booking.price "\
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


    def delete_booking(user_id):
        sql="delete from booking where member_id= %s"
        val=(user_id,)
        result=db.writeData(sql,val)
        return result

