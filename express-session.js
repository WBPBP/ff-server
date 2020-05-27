var express = require('express')
var app = express()
var parseurl = require('parseurl')
var session = require('express-session')
var bodyParser = require('body-parser')
var cookieParser = require('cookie-parser')
var SQLiteStore = require('connect-sqlite3')(session)

app.configure(function() {
  app.use(express.bodyParser.urlencoded({extended: true}));
  app.user(express.methodOverride());
  app.use(express.cookieParser());
  app.use(session({
    store: new SQLiteStore,
    secret: 'iwanttosleep', //이 값을 이용해서 세션 id 와 ...
    cookie: {maxAge: 7 * 24 * 60 * 60 * 1000}, // 1 week
  }));
});
app.use(app.router);
