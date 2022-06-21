from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
import mysql.connector
from ref.mysql_connection import get_connection

class Friends(Resource) :
    # 팔로우 하기
    @jwt_required()
    def post(self) :
        try :
            connection = get_connection()
            data = request.get_json()
            # 이메일이 존재하는지 여부 확인하기 (팔로우를 위해)
            query = '''
                        select email, nickname, id
                        from user
                        where email = %s;
                    '''
            record = (data['email'], ) # tuple
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            if len(result_list) != 1 :
                return { "result" : "입력한 사용자가 존재하지 않습니다."}

            # 이메일이 존재하면 해당 유저의 id를 팔로우
            user_id = get_jwt_identity()
            query = '''
                    insert into follow
                        (follower_id, followee_id)
                    values
                        (%s, %s);
                    '''
            record = (user_id, result_list[0]['id'])
            cursor = connection.cursor()
            follow_list = cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        return{
            "result" : "success",
            "result_list" : result_list[0]['email']+"("+result_list[0]['nickname']+") 님을 팔로우하였습니다.",
        }, 200

    # 팔로우한 친구의 메모 함께 보기
    @jwt_required()
    def get(self) :
        try :
            connection = get_connection()
            user_id = get_jwt_identity()
            query = '''select * from memo join follow where follower_id = %s;'''
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
            "result_list" : result_list
        }, 200
    