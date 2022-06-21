class Config :
    # 암호화 키
    JWT_SECRET_KEY = 'eunbyeol0413##hello' # 주의 : 노출되면 절대 안됨
    JWT_ACCESS_TOKEN_EXPIRES = False # 토큰 유지 시간
    PROPAGATE_EXCEPTIONS = True # 예외처리를 JWT로 처리