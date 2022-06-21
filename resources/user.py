import datetime
from flask import request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource
import mysql.connector
from ref.mysql_connection import get_connection
from email_validator import validate_email, EmailNotValidError
from ref.utils import check_password, hash_password

class UserRegisterResource(Resource) :
    def post(self) :
        # 데이터 교환 형식
        # {
        #     "nickname": "홍길동",
        #     "email": "abc@naver.com",
        #     "password": "1234"
        # }
        data = request.get_json()

        # 이메일 주소 형식 확인, email_validator 사용
        try :
            validate_email( data['email'] )
        except EmailNotValidError as e:
            print(str(e))
            return {'error' : str(e) }, 400
        
        # 비밀번호의 길이 유효 체크, 4~12자리
        if len(data['password']) < 4 or len(data['password']) > 12 :
            return { "error" : "비밀번호의 길이를 확인해주세요 (4-12자리)" }, 400

        # 비밀번호 암호화, passlib 사용
        hashed_password = hash_password( data['password'] )
        
        try :
            query = '''
            insert into user
                (nickname, email, password)
            values
                (%s ,%s ,%s);
            '''
            record = ( data['nickname'], data['email'], hashed_password )
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            # DB에 저장된 ID 컬럼의 값 가져오기
            user_id = cursor.lastrowid

            cursor.close()
            connection.close()

            # 'user_id' JWT 암호화
            access_token = create_access_token(user_id)

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        return {
            "result" : "success",
            "nickname" : data['nickname']+"님 회원가입이 완료되었습니다.",
            "token ID" : access_token
         }

class UserLoginResource(Resource) :
    def post(self) :
        data = request.get_json()
        connection = get_connection()

        try :
            query = '''
                        select * from user
                        where email = %s;
                    '''
            record = ( data['email'], )
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            i = 0
            for record in result_list :
                result_list[i]['created_at'] = record['created_at'].isoformat()
                i += 1
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        # result_list = 1 : 유저 데이터 존재, 0 : 데이터 없음
        if len(result_list) != 1 :
            return {"error" : "존재하지 않는 회원입니다."}, 400

        # 비밀번호 확인
        user_info = result_list[0]
        check = check_password( data['password'], user_info['password'] )
        if check == False :
            return {"error" : "비밀번호가 맞지 않습니다."}, 400

        access_token = create_access_token(user_info['id'])

        return { "result" : "success", "access_tokken" : access_token }, 200

jwt_blocklist = set()

class UserLogoutResource(Resource) :
    # jwt_required : 토큰이 있어야 아래의 코드를 실행
    @jwt_required()
    def post(self) :

        jti = get_jwt()['jti']
        print(jti)

        jwt_blocklist.add(jti)

        return { "result" : "로그아웃이 정상처리되었습니다."}