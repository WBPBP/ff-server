var {PythonShell} = require('python-shell');
var fs = require("fs");

//투입할 데이터
const testData = {
	key1: 3,
	key2: 4,
	key3: 5,
	key4: 6,
};

//문자열로 바꾼다~
var json = JSON.stringify(testData);
 
// var obj = JSON.parse(json);  얘는 복구~
// console.log(json);


//옵션을 준다
var options = {
	mode : 'text',
	encoding:'utf-8',
	pythonOptions:['-u'],
	scriptPath: '',
	pythonPath: '',
	args:[json]
};

PythonShell.run('dataProcessing.py',options,function(err,results){
	if(err){
		console.log('fail');
		console.log(err);
	}
	else{
		
	console.log('text : ',results);}
});


