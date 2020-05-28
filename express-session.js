var express = require('express')
var app = express()
var parseurl = require('parseurl')
var bodyParser = require('body-parser')
var cookieParser = require('cookie-parser')
var session = require('express-session')
//var connect = require('connect');
var sqlite3 = require('sqlite3').verbose();
var SQLiteStore = require('connect-sqlite3')(session)
const db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err);
    } else {
        //console.log('connected database in login.js ');
    }
});


  app.use(bodyParser.urlencoded({extended: true}));
  app.use(cookieParser());
  app.use(session({
    store: new SQLiteStore(session),
    secret: 'iwanttosleep', //이 값을 이용해서 세션 id 와 ...
    cookie: {maxAge: 7 * 24 * 60 * 60 * 1000}, // 1 week
	resave : false,
	saveUninitialized : true
  }));

//app.use(app.router);
