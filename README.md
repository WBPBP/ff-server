# preshoes-server

사용자의 정보와 보고서를 저장해주는 백업 서버

## 디렉토리 구조

~~~
app
  └ again                       → 이 친구는 무엇을 하는 친구일까요..?
  └ data                        →
  └ public                      →
  └ routes                      →
  └ views                       →
  └ app.js                      →
  └ dataProcessing.py           →
  └ express-session.js          →
  └ index.js                    →
  └ package.json                →
  └ README.md                   →
  └ walkData.py                 →
~~~

## 데이터베이스

데이터베이스로 **SQLite** 를 사용합니다.

테이블 구조는 다음과 같습니다.

### USER

**사용자의 정보들이 들어가는 테이블**

- `user_email`: 이메일 주소
- `user_pwd`: 해싱 처리된 비밀번호
- `user_gender`: 성별
- `user_age`: 나이
- `user_weight`: 체중
- `user_height`: 키

### REPORT

**사용자의 계정과 보고서 파일명이 저장된 테이블**

- `user_emal`: 이메일 주소
- `file_name`: 파일명


## API

### POST /join/addUser

**회원가입**

#### 요청 모델

`application/json`

- `user_email`: 이메일 주소
- `user_pwd`: 비밀번호
- `user_gender`: 성별
- `user_age`: 나이
- `user_weight`: 체중
- `user_height`: 키

#### 응답 코드

- 201: 회원가입 성공
- 400: 이메일 형식에 문제가 있음
- 401: 이메일이 이미 존재함

#### 응답 모델

없음


### POST /login

#### 요청 모델

`application/json`

- `user_email`: 이메일 주소
- `user_pwd`: 비밀번호

#### 응답 코드

- 200: 사용자가 존재하며 비밀번호가 올바름
- 400: 로그인 실패
- 401: 사용자가 존재하지 않음
- 500: 서버 내부 에러

#### 응답 모델

없음


### GET /logout

**로그아웃**

세션 반환 후 홈화면으로 돌아감

#### 요청 모델

없음

#### 응답 코드

- 200: 성공
- 500: 서버 내부 에러

#### 응답 모델

없음


### Delete /delete

**회원 삭제**

#### 요청 모델

-

#### 응답 코드

- 200: 삭제 성공
- 401: 사용자가 존재하지 않음

#### 응답 모델

-

### POST /send/info

**보고서 생성 및 저장 후 안드로이드에게 파일 전송**

안드로이드에서의 입력값을 json파일로 변환 후 파이썬파일에 있는 함수 리턴값을 다시 가져와서 그 내용을 보고서파일로 작성 후 안드로이드에 전송

파일명은 만들어지는 당시의 날짜+시간으로 생성.    
유저의 이메일과 파일명으로 `user.db`의 `report` table에 저장     

#### 요청 모델

-

#### 응답 코드

-

#### 응답 모델

-
