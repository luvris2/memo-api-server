from passlib.hash import pbkdf2_sha256 # 암호화, 일반적으로 사용 sha256

# 원문 비밀번호를 암호화 하는 함수
# hash : 암호화 하는 함수
def hash_password(original_password) :
    salt = 'yh*hello12'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password

# 비밀번호가 맞는지 확인하는 함수
# verify : 두 데이터가 동일하는지 확인하는 함수
def check_password(original_password, hashed_password) :
    salt = 'yh*hello12'
    check = pbkdf2_sha256.verify(original_password+salt, hashed_password)
    return check # Return value : True/False