var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var validator = require('validator');
var crypto = require('crypto');
const db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err);
    } else {
        //console.log('connected database in join.js ');
    }
});

/* GET users listing. */
router.get('/', function (req, res, next) {
    res.render('join');
	
});

router.post('/addUser',function(req,res,next){

   var key = 0; //중복여부 키 
   //회원가입에 들어갈 정보들 
   const id = (req.body.user_email).toLowerCase();
   console.log(id);
	const pwd = req.body.user_pwd;
	crypto.randomBytes(32,function(err,buffer){
		if(err){
			res.sendStatus(500);
		}
		else{
			let salt = buffer.toString('base64');
			crypto.pbkdf2(req.body.user_pwd,salt,100000,64,'sha512',function(err,hashed){
				let saltPWD=hashed.toString('base64');
				const query = `insert into user(user_email, user_pwd,salt) values (?,?,?)`;				
				//정보기입후 아이디 중복 검사
				db.all('SELECT * FROM user WHERE user_email = ?',id,function(err,db_data){ //그 아이디가 있는지 확인 
					
					db_result=db_data;						
					if(validator.isEmail(id)){
						if(db_result==0){
							key=1;
						}
						else{
										  
							console.log('sorry, that ID is already existed');
							res.sendStatus(400); // 잘못된 요청 
							}
					}
					else{
						console.log('wrong form of email');
						res.sendStatus(400);	//서버가 요청 구문 인식 못함 	 
					}
									  
					if( key === 1){ //중복이 아니므로
						db.run(query,id,saltPWD,salt,function(err,db_data){ //인서트 하고 성공했다는 메세지 보내준다. 
							console.log('insert user table :',id);
							res.sendStatus(201); //created
						});
					}
					else { //아님 페일 
						console.log('sign up failure'); 
						
					}
				});								
			});
		}	
	});



});

module.exports = router;