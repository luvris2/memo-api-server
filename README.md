# memo-api-server

# 메모장
**기능 설명**
- 로그인, 로그아웃 기능
- 메모 작성, 수정, 삭제 기능
- 자신의 메모 보기 기능, 다른 사람은 열람 불가
- 팔로우한 친구의 메모 공유
---
# DB 구조
### Table : user
- Columns
  - id : 기본 인덱스 (INT/ PK, NN, UN, AI)
  - email : 이메일 (VARCHAR(45)/ UQ)
  - password : 비밀번호 (VARCHAR256)
  - nickname : 사용자 이름 (VARCHAR45)
  - created_at : 생성일자 (TIMESTAPM) / Default=now()
### Table : memo
- Columns
  - id : 기본 인덱스 (INT/ PK, NN, UN, AI)
  - title : 메모의 제목 (VARCHAR(45)
  - date : 이행 시간 (VARCHAR(45)
  - content : 메모 내용 (VARCHAR(256)
  - created_at : 메모 생성일 (TIMESTAMP)/ Default=now()
  - updated_at : 메모 수정일 (TIMESTAMP)/ Default=now() on update now()
  - user_id : Foreign Key Value (INT/ NN, UN)
- Foreign Keys
  - memo table : user_id -> user table : id
### Table : follow
- Columns
    - id : 기본 인덱스 (INT/ PK, NN, UN, AI)
    - follower_id : 팔로우한 사람 (INT/ UN)
    - followee_id : 팔로우 당한 사람 (INT/ UN)
    - created_at : 팔로우 일자 (TIMESTAMP)/ Default=now()
- Foreign Keys
  - follow table : follower_id -> user table : id
  - follow table : followee_id -> user table : id
- Indexes
  - Type : UNIQUE
  - Column : follower_id, followee_id
---

# 파일 구조
- app.py : API 메인 파일
  - resources 폴더
    - follow.py : 친구 관련 기능
    - memo_modify.py : 메모 작성, 수정, 열람, 삭제 기능
    - user.py : 회원가입, 로그인, 로그아웃 기능
  - ref 폴더
    - config.py : 가상환경 설정 (토큰)
    - mysql_connection.py : DB 연동 설정
    - utils.py : 비밀번호 암호화, 식별 ID 토큰화 설정

---

# 각 파일 설명
**app.py**
- API의 기본 틀이 되는 메인 파일
- 가상 환경 셋팅
- JWT 토큰을 생성과 파괴
- 리소스화 된 클래스들의 경로 설정 (API 기능)

---

**mysql_connection.py**
- DB 연동에 관련된 함수를 정의한 파일
  - 해당 코드는 개개인의 환경에 따라 다르므로 파일은 미첨부
  - 아래의 코드로 파일을 생성하여 자신의 환경에 맞게 코딩
``` python
import mysql.connector
def get_connection() :
    connection = mysql.connector.connect(
        host='hostname',
        database='databasename',
        user='username',
        password='password' )
    return connection
```

---

**config.py**
- 가상 환경의 값을 설정하는 파일
  - 토큰의 암호화 방식 설정
    - 토큰의 시크릿 키는 원래 비공개이나 테스트용이기 때문에 공개처리
    - 토큰은 유저의 개인 식별 ID를 암호화하여 사용

**utils.py**
- 사용자로부터 입력받은 비밀번호를 암호화하는 파일
  - 입력 받은 비밀번호를 해시로 매핑하여 암호화
  - 암호화된 비밀번호와 새로 입력 받은 값이 같은지 확인

---

**user.py**
- Class UserRegisterResource
  - 회원가입을 하면 DB에 입력한 정보가 등록되는 기능
    - 이메일과 비밀번호 유효성 검사
    - 비밀번호 암호화, 식별 ID 토큰화
- class UserLoginResource
  - 로그인
    - DB에 입력한 이메일 존재 유무와 비밀번호 동일 유무 확인
    - 입력한 데이터가 DB의 정보와 일치하면 식별 ID 토큰 생성
- class UserLogoutResource
  - 로그아웃
    - 생성된 토큰을 파괴  

---

 **memo_modify.py**
- class MemoResource
  - 입력한 메모를 작성
  - 작성한 메모 조회
    - 다른 사람의 메모는 조회 불가
- class MemoModifyResource
  - 작성한 메모 수정
    - 친구의 메모는 조회만 가능하며, 수정은 불가
  - 작성한 메모 삭제
    - 삭제 또한 친구의 메모는 삭제 불가

**follow.py**
- class Friends
    - 팔로우
      - 이메일 존재 유무 확인
      - 이메일이 존재하면 팔로우
    - 팔로우한 친구의 메모 함께 보기
      - 팔로우한 친구(followee)의 메모와 내 메모를 함께 리스트로 출력
    - 팔로우 해제
      - 팔로우 테이블의 데이터를 삭제
      - 팔로우를 해제하면 상대와 나의 메모가 보이지 않음