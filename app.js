var express = require('express');
var app = express(); //express 만든 사람이 이렇게 사용해라 약속
var bodyParser = require('body-parser');
var session = require('express-session');
var FileStore = require('session-file-store')(session);
app.use(express.static('public'));//관습적으로 public
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:true}))

  app.use(session({
    secret: 'iwanttosleep', //이 값을 이용해서 세션 id 와 ...
	resave : false,
	saveUninitialized : true,
	store: new FileStore()
  }));


var joinRouter = require('./routes/users/join');
app.use('/join',joinRouter);

var loginRouter = require('./routes/users/login');
app.use('/log',loginRouter);

var sendingRouter = require('./routes/reports/send');
app.use('/send',sendingRouter);

var deleteRouter = require('./routes/users/delete');
app.use('/delete',deleteRouter);



 app.listen(3000, function(){
	 
   console.log('Connected WBPBP 3000 port!');
 });