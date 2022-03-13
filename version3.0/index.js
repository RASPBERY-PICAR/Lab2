
// redefine the onkeydown and onkeyup event
document.onkeydown =new_update_key;
document.onkeyup = new_reset_key;

var address = "E4:5F:01:42:E0:84";
var data_flag=null;
var key_flag=null;
var btSerial = new (require('bluetooth-serial-port')).BluetoothSerialPort();

// called in the html
// change the bluetooth connection state
function connection_update(){
    console.log('change connection status');
    if (document.getElementById("connection").value == "ON") {
        disconnect_bt();
        document.getElementById("connection").value = "OFF";
        document.getElementById("connection").innerHTML = "OFF";
    } else {
        connect_bt();
        document.getElementById("connection").value = "ON";
        document.getElementById("connection").innerHTML = "ON";
    }
}

// called in the html
// change the state of the updating data, can update data in period or stop updating
function data_update(){
    console.log('update data');
    if (document.getElementById("update").value == "ON") {
        document.getElementById("update").value = "OFF";
        clearInterval(data_flag);
        data_flag=null;
        document.getElementById("update").innerHTML = "OFF";
    } else {
        document.getElementById("update").value = "ON";
        document.getElementById("direction").innerHTML = "Stop";
        data_flag=setInterval(function(){polling_data();}, 1000);
        document.getElementById("update").innerHTML = "ON";
    }
}

// called in the html
// change the state of streaming, start or end the real-time stream
function stream_update(){
    console.log('update stream status');
    if (document.getElementById("stream").value == "ON") {
        document.getElementById("stream").value = "OFF";
        send_cmd('stm_ed\r\n');
        document.getElementById("stream").innerHTML = "OFF";
    } else {
        document.getElementById("stream").value = "ON";
        send_cmd('stm_st\r\n');
        document.getElementById("stream").innerHTML = "ON";
    }    
}

// helpfunction
// connect to picar by bluetooth 
function connect_bt(){
    btSerial.connect(address, 1, function() {
        console.log('connected');
        document.getElementById("bluetooth").innerHTML =  'connected'; 
      });
}

// helpfunction
// disconnect
function disconnect_bt(){
    send_cmd('quit\r\n')
    btSerial.close();
    console.log('disconnected');
    document.getElementById("bluetooth").innerHTML =  'disconnected';  
}

// helpfunction 
// update pi's data one time
function polling_data(){
    btSerial.write(Buffer.from('polling\r\n', 'utf-8'), function(err, bytesWritten) {
        if (err) {
            console.log('Error!');
        } 
    });
    btSerial.on('data', function(buffer) {
        var s_list = buffer.toString().split(",");
        var b_status = s_list[0];
        var t_status = s_list[1];
        var distance = s_list[2];
        document.getElementById("battery").innerHTML =  b_status;
        document.getElementById("temperature").innerHTML = t_status;
        document.getElementById("distance").innerHTML = distance;
        console.log(b_status,t_status);
    });
    document.getElementById("bluetooth").innerHTML =  'done';      
}   


// helpfunction 
// send one command to pi
function send_cmd(cmd){
    btSerial.write(Buffer.from(cmd, 'utf-8'), function(err, bytesWritten) {
        if (err) {
            console.log('Error!');
        } 
    });
}

// helpfunction
// update key in period
function new_update_key(e){
    if (key_flag == null) {
        updateKey(e);
        key_flag=setInterval(function(){updateKey(e);}, 500);
    }
}

// helpfunction
// stop updating key in period and reset
function new_reset_key(e){
    if (key_flag != null) {
        clearInterval(key_flag);
        key_flag=null;
    }
    resetKey(e);
}

// helpfunction
// send cmd when direction keys are pressed and show the state in web
function updateKey(e) {
    e = e || window.event;
    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        document.getElementById("direction").innerHTML = "Forward";
        send_cmd('87\r\n');
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        document.getElementById("direction").innerHTML = "Backward";
        send_cmd('83\r\n');
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        document.getElementById("direction").innerHTML = "Turn Left";
        send_cmd('65\r\n');
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        document.getElementById("direction").innerHTML = "Turn Right";
        send_cmd('68\r\n');
    }
    else if (e.keyCode == '81') {
        // stop
        document.getElementById("direction").innerHTML = "Stop";
        send_cmd('81\r\n');
    }
}

// helpfunction
// reset the key and send smd to stop the car
function resetKey(e) {
    e = e || window.event;
    send_cmd('81\r\n');
    document.getElementById("direction").innerHTML = "Stop";
    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}

