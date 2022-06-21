from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
import mysql.connector
from ref.mysql_connection import get_connection

class MemoResource(Resource) :
    # 메모 작성하기
    @jwt_required()
    def post(self) :
        data = request.get_json()
        user_id = get_jwt_identity()
        try :
            connection = get_connection()
            query = '''
                    insert into memo
                        (title, date, content, user_id)
                    values
                        (%s, %s, %s, %s);
                    '''
            record = (data['title'], data['date'], data['content'], user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        return {"result" : "success"}, 200

    # 자신의 메모 조회
    @jwt_required()
    def get(self) :
        try :
            connection = get_connection()
            user_id = get_jwt_identity()
            query = '''
                        select *
                        from memo
                        where user_id = %s;
                    '''
            record = (user_id, ) # tuple
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            i = 0
            for record in result_list :
                result_list[i]['created_at'] = record['created_at'].isoformat()
                result_list[i]['updated_at'] = record['updated_at'].isoformat()
                i += 1
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        return{
            "result" : "success",
            "count" : len(result_list),
            "result_list" : result_list
        }, 200


class MemoModifyResource(Resource) :
    # 메모 수정하기
    @jwt_required()
    def put(self, memo_id) :
        data = request.get_json()
        try :
            connection = get_connection()
            user_id = get_jwt_identity()
            query = '''select user_id from memo where id = %s;'''
            record = (memo_id, )
            cursor = connection.cursor(dictionary = True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            memo = result_list[0]

            if memo['user_id'] != user_id :
                cursor.close()
                connection.close()
                return { "error" : "수정할 수 없습니다."}

            query = '''
                    update memo set
                        title=%s, date=%s, content=%s
                    where id = %s;
                    '''
            record = (data['title'], data['date'], data['content'], memo_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        return {"result" : "success"}, 200


    # 데이터를 삭제하는 API들은 delete 함수를 사용한다.
    def delete(self, memo_id) :
        data = request.get_json()
        try :
            connection = get_connection()
            query = '''
                    delete from memo
                    where id = %s;
                    '''
            record = (memo_id, )
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE
        return {"result" : "success"}, 200