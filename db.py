import pymysql


class Database:
    connection = pymysql.connect(
        host='localhost',
        user='',
        password='',
        db='tgbot',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    if connection:
        print('Connection Succesfull')
    else:
        print('No connection!')

    def select(self, user_id, ):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM palmabot WHERE `user_id` = %s "
            cursor.execute(query, (user_id))
            row = cursor.fetchall()
            if len(row) > 0:
                return row[0]
            else:
                return None

    def add(self, name, first_name, count, user_id):
        with self.connection.cursor() as cursor:
            query = "INSERT INTO palmabot (`user`, `first_name` , `growth`, `user_id`) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, first_name, count, user_id))
            self.connection.commit()

    def update(self, user_id,date, palma):
        with self.connection.cursor() as cursor:
            query = "UPDATE palmabot SET growth = growth + %s , date = %s WHERE user_id = %s"
            cursor.execute(query, (palma, date, user_id))
            self.connection.commit()


database = Database()
