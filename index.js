var express - require('express')
var app = express(); //express 만든 사람이 이렇게 사용해라 약속
var router = express.Router()
var path = require('path')
var sqlite3 = require('sqlite3');
var db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db');

router.get('/', function(req,res){
	console.log('get join url');
	res.render('join.ejs');
})


router.post('/',function(req,res){
	var body = req.body;
	var email = body.email;
	//var name = body.name;
	var passwd = body.passwd;
	
	var sql = {email.email,pw : passwd};
	var query = connection.query('insert into user set?',sql,function(err,rows)
		if(err) throw err
		else res.render('welcome,ejs',{'id': rows.insertId}
})
		
	
})

module.exports = router;