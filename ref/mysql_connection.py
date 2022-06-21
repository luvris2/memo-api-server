import mysql.connector

def get_connection() :
    connection = mysql.connector.connect(
        host='yh-db.ccekp8a5rlv0.ap-northeast-2.rds.amazonaws.com',
        database='memo_db',
        user='memo_db_admin',
        password='memo_administrator' )
    return connection
