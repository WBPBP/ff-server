var {PythonShell} = require('python-shell');
var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err);
    } 
	else {
    }
});

router.get('/', function (req, res, next) {
    res.render('send');
	
});

//투입할 데이터 안드로이드에서 오면 나 이거 삭제해도됨


//문자열로 바꾼다~

 
// var obj = JSON.parse(json);  얘는 복구~
// console.log(json);





router.post('/info',function(req,res,next){
//옵션을 준다
	var date = new Date();
	function getFormatDate(date){
		var year = date.getFullYear();              //yyyy
		var month = (1 + date.getMonth());          //M
		month = month >= 10 ? month : '0' + month;  //month 두자리로 저장
		var day = date.getDate();                   //d
		day = day >= 10 ? day : '0' + day;          //day 두자리로 저장
		var hour =date.getHours();
		hour = hour >=10 ? hour : '0'+ hour;
		//hour 두자리로 저장	
		var minute =date.getMinutes();
		minute= minute >=10 ? minute : '0'+ minute;
		//minute 두자리로 저장
		var second =date.getSeconds();
		second = second >=10 ? second : '0'+ second;
		//second 두자리로 저장
		return  year + '' + month + '' + day+'_'+hour+''+minute+''+second;
	}
	const features = req.body;
	if (features.verticalWeightBias_Left && features.verticalWeightBias_Right && features.horizontalWeightBias && features.heelPressureDifference && features.leftPressure && features.rightPressure){
		
		var json = JSON.stringify(features);
		var options = {
			mode : 'text',
			encoding:'utf-8',
			pythonOptions:['-u'],
			scriptPath: '',
			pythonPath: '',
			args:[json]
		};
		date = getFormatDate(date);
		PythonShell.run('/home/ec2-user/myapp/model/Execute.py',options,function(err,results){
			if(err){
				console.log('fail');
				console.log(err);
				res.sendStatus(500);
			}
			else if(req.session.displayName){
				console.log(req.session.displayName);			
				console.log('잘 넘어갔다왔음');		
				db.all('SELECT user_id from user WHERE user_email = ?',req.session.displayName, function(err,db_data){
					if(err){
						res.sendStatus(500);
						console.log('here is problem');
					}
					else{
						user_id= db_data[0].user_id;
						const query =`insert into report (user_id,contents)values('${user_id}','${results}')`;
						db.run(query,function(err,db_data){ //인서트 하고 성공했다는 메세지 보내준다. 
							res.json(results);
							console.log('보고서 완료');
						}); 
								
							}
						});
				
			}
			else{
				console.log('session is expired');
				res.sendStatus(401); //권한없음 
			}
		});
	}
	else res.sendStatus(400);
});	
	

 module.exports = router;


