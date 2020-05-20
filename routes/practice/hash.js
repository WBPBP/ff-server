var bcrypt = require('bcryptjs');
bcrypt.genSalt(10,function(err, salt){
	bcrypt.hash("password", salt, function(err, hash){
	});
});

bcrypt.compare("password",hash function(err, res){
	if(res){
		console.log("login success")
	}else{
	console.log("login failure")}
		

});
 