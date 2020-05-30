# preshoes-server

사용자의 정보와 보고서를 저장해주는 백업 서버

## 디렉토리 구조

~~~
app
  └ data                        →
  └ routes                      →
  └ app.js                      →
  └ model                       →
  └ package.json                →
  └ README.md                   →
  └ sessions                    →
~~~

## 데이터베이스

데이터베이스로 **SQLite** 를 사용합니다.

테이블 구조는 다음과 같습니다.

### USER

**사용자의 정보들이 들어가는 테이블**

- `user_email`: 이메일 주소 (text)
- `user_pwd`: 해싱 처리된 비밀번호 (text)
- `salt` : 비교해야하는 salt 값 (text)

### REPORT

**사용자의 계정과 보고서 파일명이 저장된 테이블**

- `user_id`: 이메일 주소 (text)
- `contents`: 파일 내용 (json) 


## API

### POST /join/addUser

**회원가입**

#### 요청 모델

`application/json`

- `user_email`: 이메일 주소 (text)
- `user_pwd`: 비밀번호 (text)
- `salt` : 비교해야하는 salt 값 (text)

#### 응답 코드

- 201: 회원가입 성공
- 400: 이메일 형식에 문제가 있음
- 401: 이메일이 이미 존재함

#### 응답 모델

없음


### POST /log/in

#### 요청 모델

`application/json`

- `user_email`: 이메일 주소 (text)
- `user_pwd`: 비밀번호 (text)
- `salt` : 비교해야하는 salt 값 (text)

#### 응답 코드

- 200: 사용자가 존재하며 비밀번호가 올바름
- 400: 로그인 실패
- 401: 사용자가 존재하지 않음
- 500: 서버 내부 에러

#### 응답 모델

없음


### GET /log/out

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

안드로이드에서의 입력값을 json파일로 변환 후 파이썬파일에 있는 함수 리턴값을 다시 가져와서 그 내용을 안드로이드에 전송 후 db에 저장

파일명은 만들어지는 당시의 날짜+시간으로 생성.    
유저의 id와 파일내용으로 `user.db`의 `report` table에 저장     

#### 요청 모델
 - json     
 {    
    "verticalWeightBias_Left" : "double",    
    "verticalWeightBias_Right" : "double",   
    "horizontalWeightBias" : "double",    
    "heelPressureDifference" : "int",    
    "leftPressure" : "int[]",    
    "rightPressure" : "int[]"    
 }    


#### 응답 코드

-

#### 응답 모델
json    
{    
   "staticPressureRes" : "string",    
   "percent" : "int",     
   "gaitComment" : "string",     
   "diseaseNum" : "int"     
}    

-
