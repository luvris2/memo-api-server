# 데이터베이스에 접속해서 데이터 처리하는 테스트 코드
import mysql.connector
from ref.mysql_connection import get_connection

try :
    connection = get_connection()

    var = ''
    query = '''
            insert into recipe
                (name, description, cook_time, direction)
            values
                (%s ,%s ,%s ,%s);
            '''
    record = (var, )

    # 3. Get Cursor
    cursor = connection.cursor()

    # 4. Execute Query with cursor
    cursor.execute(query, record)

    # 5. DATA commit
    connection.commit()

    # 6. Close Resource
    cursor.close()
    connection.close()

except mysql.connector.Error as e :
    print(e)