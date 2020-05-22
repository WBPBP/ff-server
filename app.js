var express = require('express');
var app = express(); //express 만든 사람이 이렇게 사용해라 약속
var bodyParser = require('body-parser');
//var session = require('express-session')
//var SQLiteStore = require('connect-sqlite3')(session)
app.locals.pretty= true;
app.use(express.static('public'));//관습적으로 public
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:true}))
var PythonShell = require('python-shell');



var joinRouter = require('./routes/users/join');
app.use('/join',joinRouter);

var loginRouter = require('./routes/users/login');
app.use('/login',loginRouter);

var sendingRouter = require('./routes/reports/send');
app.use('/send',sendingRouter);


// app.configure(function(){
// app.use(express.bodyParser());	
// app.use(express.cookieParser());  
// app.use(session({
  // store: new SQLiteStore,
  // secret: 'iwanttosleep',
  // cookie : {maxAge : 7*24*60*60*1000} // 1 week
  // //resave: false,
  // //saveUninitialized: true
// }));

// });


 app.listen(3000, function(){
	 
   console.log('Connected WBPBP 3000 port!');
 });
 
 module.exports = app;