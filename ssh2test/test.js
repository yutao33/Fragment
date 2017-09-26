var Client=require('ssh2').Client;

var conn=new Client();


var i = 0;
var j = 0;
var k = 1;

conn.on('ready',function(){
	console.log('ready')
	test();
}).connect({
	host:'localhost',
	port:8101,
	username:'karaf',
	password:'karaf'
});

function test(){
	var num;
	if(k==1){
		num=-1;
		k=2;
	} else if(k==2){
		num=(i+1)*10000;
		k=3;
		j++;
		if(j==3){
			j=0;
			i++;
		}
	} else if(k==3){
		num=-2;
		k=1
	}


	cmd = 'test-command -tA '+num;

	console.log(cmd);

	conn.exec(cmd,function(err,stream){
		if(err)throw err;
		stream.on('data',function(data){
			console.log(data.toString());
		}).on('close',function(code,signal){
			console.log('close');
			if(i<10){
				if(k==1){
					console.log("=====================");
				}
				if(k==3){
					setTimeout(test,15000+i*1000);
				} else {
					test();
				}
			}
		});
	})
}