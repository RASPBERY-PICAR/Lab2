document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "172.20.10.3";   // the IP address of your Raspberry PI

function client(){
    
    const net = require('net');
    var input = document.getElementById("message").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        var s_list = data.toString().split(",");
        var b_status = s_list[0];
        var t_status = s_list[1];
        // document.getElementById("bluetooth").innerHTML = data;
        document.getElementById("battery").innerHTML = b_status;
        document.getElementById("temperature").innerHTML = t_status;
        // console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function key_client(val) {
    const net = require('net');
    
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${val}\r\n`);
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        document.getElementById("direction").innerHTML = "Forward";
        key_client('87');
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        document.getElementById("direction").innerHTML = "Backward";
        key_client('83');
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        document.getElementById("direction").innerHTML = "Turn Left";
        key_client('65');
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        document.getElementById("direction").innerHTML = "Turn Right";
        key_client('68');
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}


// update data for every 50ms
function update_data(){
    setInterval(function(){
        // get image from python server
        client();
    }, 1000);
}




// bluetooth

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

function update_data_bt(){
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



