import pymysql


class Database:
    connection = pymysql.connect(
        host='localhost',
        user='',
        password='',
        db='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    if connection:
        print('Connection Succesfull')
    else:
        print('No connection!')

    def select(self, user_id, chat_id):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM palmabot WHERE `user_id` = %s AND `chat_id` = %s"
            cursor.execute(query, (user_id,chat_id))
            row = cursor.fetchall()
            if len(row) > 0:
                return row[0]
            else:
                return None

    def add(self, name, first_name, count, user_id,chat_id):
        with self.connection.cursor() as cursor:
            query = "INSERT INTO palmabot (`user`, `first_name` , `growth`, `user_id`, `chat_id`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, first_name, count, user_id,chat_id))
            self.connection.commit()

    def update(self, user_id,date, palma):
        with self.connection.cursor() as cursor:
            query = "UPDATE palmabot SET growth = growth + %s , date = %s WHERE user_id = %s"
            cursor.execute(query, (palma, date, user_id))
            self.connection.commit()

    def select_top(self,chat_id):
        with self.connection.cursor() as cursor:
            query= "SELECT * FROM palmabot WHERE chat_id = %s ORDER BY `growth` DESC"
            cursor.execute(query, (chat_id))
            self.connection.commit()
            row = cursor.fetchall()
            return row


database = Database()
