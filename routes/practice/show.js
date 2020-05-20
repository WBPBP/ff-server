var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err);
    } else {
        console.log('connected database in show.js');
    }
});

router.get('/', function (req, res, next) {
    res.render('show');
});
//모든애들 다 보여주는거 
router.get('/allUser',function(req,res){
	  db.serialize();
    db.all('SELECT * FROM user',function(err,db_data){
       db_result = db_data;
       console.log('Get all User');
      res.send(db_result);
    });
});
// 선택된 애들만 보여주는고 
router.post('/getUser', function(req,res){
   var user = req.body.user_name;
     db.serialize();
   db.each('SELECT * FROM user WHERE user_name = ?',user,function(err,db_data){
      db_result = db_data;
      console.log("getUser : " +user);
      console.log(db_result);
      res.send(db_result);
   });
});

module.exports = router;