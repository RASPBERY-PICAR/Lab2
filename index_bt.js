//document.onkeydown = updateKey;
//document.onkeyup = resetKey;
//const bluetooth = require('node-bluetooth');
 
// create bluetooth device instance
// const device = new bluetooth.DeviceINQ();
//var address = "E4:5F:01:42:E0:84";

// function clientbt(){
  
//   const bluetooth = require('node-bluetooth');
 
//   // create bluetooth device instance
//   // const device = new bluetooth.DeviceINQ();
//   var address = "E4:5F:01:42:E0:84";
// // make bluetooth connect to remote device
//    var input = document.getElementById("message").value;
//   bluetooth.connect(address, 1, function(err, connection){
//     if(err) return console.error(err);
//     connection.write(new Buffer('${input}\r\n', 'utf-8'), () => {
//       console.log("wrote");
//     });
//     // connection.write(`${input}\r\n`);
//     // connection.on('data', (buffer) => {
//     //   console.log('received message:', buffer.toString());
//     // });

//     //get the data from the server
//     connection.on('data', (buffer) => {
//       console.log('received message:', buffer.toString());
//         var s_list = buffer.toString().split(",");
//         var b_status = s_list[0];
//         var t_status = s_list[1];
//         document.getElementById("battery").innerHTML = b_status;
//         document.getElementById("temperature").innerHTML = t_status;
//         console.log(b_status,t_status);
//     });
    
//   });
// }


function clientbt(){
  
var btSerial = new (require('bluetooth-serial-port')).BluetoothSerialPort();
 
  // create bluetooth device instance
  // const device = new bluetooth.DeviceINQ();
var address = "E4:5F:01:42:E0:84";
// make bluetooth connect to remote device
   var input = document.getElementById("message").value;   
  btSerial.connect(address, 1, function() {
    console.log('connected');
  
    btSerial.write(Buffer.from('Begin\r\n', 'utf-8'), function(err, bytesWritten) {
      if (err) console.log(err);
    });
	console.log('written data');
    btSerial.on('data', function(buffer) {
      //console.log(buffer.toString('utf-8'));
      var s_list = buffer.toString().split(",");
        var b_status = s_list[0];
        var t_status = s_list[1];
        document.getElementById("battery").innerHTML = b_status;
        document.getElementById("temperature").innerHTML = t_status;
        console.log(b_status,t_status);
    });
    
  },function () {
			console.log('cannot connect');
		});
  console.log('pre close');
  setTimeout(btSerial.close(), 1000);
  if (btSerial.isOpen()) {
 		console.log('fail to close');
 	}
  console.log('close')
}   

function clientbt_connect(){
  
var btSerial = new (require('bluetooth-serial-port')).BluetoothSerialPort();
 
  
var address = "E4:5F:01:42:E0:84";
// make bluetooth connect to remote device
   var input = document.getElementById("message").value;   
  btSerial.connect(address, 1, function() {
    console.log('connected');
  
    btSerial.write(Buffer.from("Begin\r\n", 'utf-8'), function(err, bytesWritten) {
      if (err) console.log(err);
    });
	console.log('written data');
    
    
  },function () {
			console.log('cannot connect');
		});
  //console.log('pre close');
  //setTimeout(btSerial.close(), 1000);
  //if (btSerial.isOpen()) {
 		//console.log('fail to close');
 	//}
  //console.log('close')
  return btSerial;
}

function client_read(btSerial){
	var s_list;
	btSerial.on('data', function(buffer) {
      //console.log(buffer.toString('utf-8'));
       var s_list = buffer.toString().split(",");
        var b_status = s_list[0];
        var t_status = s_list[1];
        if (document.getElementById("update").value == "ON") {
		document.getElementById("battery").innerHTML = b_status;
		document.getElementById("temperature").innerHTML = t_status;
        }
        else {
        	document.getElementById("battery").innerHTML = "";
		document.getElementById("temperature").innerHTML = "";
        }
        console.log(b_status,t_status);
        return s_list;
        });
        
        return s_list;

}
function disconnect(btSerial){
	btSerial.close();
}

function update_data(){
 var flag;
 
 
     console.log('update_data');
     if (document.getElementById("update").value == "ON") {
	console.log('change on to off');
         //document.getElementById("update").value = "OFF";
         //clearInterval(flag)
         document.getElementById("battery").innerHTML = "";
        document.getElementById("temperature").innerHTML = "";
         console.log('close');
         
         document.getElementById("update").value = "OFF"
      
     } else {
     	console.log('enter else state');
         
         document.getElementById("update").value = "ON"
         var btSerial = clientbt_connect();
         
          // get image from python server
          client_read(btSerial);
          //clientbt();
          
          disconnect(btSerial);
      
     }
     
     
    
     // document.getElementById("battery").innerHTML = "1";
     // setInterval(function(){
     //     // get image from python server
     //     client();
     // }, 1000);
}


