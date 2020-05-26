# preshoes-server
사용자의 정보와 보고서를 저장해주는 백업 서버

## database
### user.db

#### tables
- user : 사용자의 정보들이 들어가는 테이블    
이메일주소 : user_email    
해싱처리된 비밀번호 : user_pwd    
salt 값(입력받지는 않음) : salt    
성별 : user_gender    
나이 : user_age    
몸무게 : user_weight    
키 : user_height    

- report : 사용자의 계정과 보고서 파일명이 저장된 테이블    
이메일 주소 : user_email    
파일명 : file_name    



## API

### GET

- /logout : 로그아웃     
세션 반환 후 홈화면으로 돌아감 

### POST

- /join/addUser :회원가입    
이메일주소 : user_email    
해싱처리된 비밀번호 : user_pwd    
salt 값(입력받지는 않음) : salt    
성별 : user_gender    
나이 : user_age    
몸무게 : user_weight    
키 : user_height    

로 입력값을 받고 있으며 json 형식 사용     
이메일 중복확인 절차     
이메일 형식이 아닐 경우 ->400    
이미 있는 이메일일 경우 ->401    
생성 성공 ->201    


- /login : 로그인 

서버오류 ->500    
이메일이 존재하지 않으면(회원가입이 안되어있으면) ->401    
이메일이 있으면 비밀번호 검사 후 맞으면 ->200     
로그인 실패 ->400     


- /send/info : 보고서 생성 및 저장 후 안드로이드에게 파일 전송 

안드로이드에서의 입력값을 json파일로 변환 후 파이썬파일에 있는 함수 리턴값을 다시 가져와서 그 내용을 보고서파일로 작성 후 안드로이드에 전송 

파일명은 만들어지는 당시의 날짜+시간으로 생성.    
 유저의 이메일과 파일명으로 user.db report table에 저장     



### DELETE

- /delete :  회원삭제 

지우고자 하는 이메일 없으면->401     
삭제하고 db 회원 시퀀스 초기화 후-> 200    
세션이 만들어지면 입력값을 이메일로 받지 않고 세션을 넘겨줄 예정
