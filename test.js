var PythonShell = require('Python-shell');
var options = {
	mode : 'text',
	encoding:'ufc-8',
	pythonOptions:['-u'],
	scriptPath: '',
	pythonPath: '',
	args:['value1','value2','value3']
	
};

PythonShell.run('test.py',options,function(err,results){
	if(err) throw err;
	console.log('results : %j',results);
});
