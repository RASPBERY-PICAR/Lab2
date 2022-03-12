var flag=null;

document.onkeydown =period_up;
document.onkeyup = period_reset;

var server_port = 65432;
var server_addr = "172.20.10.3";   // the IP address of your Raspberry PI
// var server_addr = "192.168.0.35";

function period_up(e){
    if (flag == null) {
        updateKey(e);
        flag=setInterval(function(){updateKey(e);}, 1000);
    }
}

function period_reset(e){
    if (flag != null) {
        clearInterval(flag);
        flag=null
    }
    resetKey(e);
}

// function client(){
    
//     const net = require('net');
//     var input = document.getElementById("message").value;

//     const client = net.createConnection({ port: server_port, host: server_addr }, () => {
//         // 'connect' listener.
//         console.log('connected to server!');
//         // send the message
//         client.write(`${input}\r\n`);
//     });
    
//     // get the data from the server
//     client.on('data', (data) => {
//         var s_list = data.toString().split(",");
//         var b_status = s_list[0];
//         var t_status = s_list[1];
//         // document.getElementById("bluetooth").innerHTML = data;
//         document.getElementById("battery").innerHTML = b_status;
//         document.getElementById("temperature").innerHTML = t_status;
//         // console.log(data.toString());
//         client.end();
//         client.destroy();
//     });

//     client.on('end', () => {
//         console.log('disconnected from server');
//     });
// }

// function key_client(val) {
//     const net = require('net');
    
//     const client = net.createConnection({ port: server_port, host: server_addr }, () => {
//         // 'connect' listener.
//         console.log('connected to server!');
//         // send the message
//         client.write(`${val}\r\n`);
//     });

//     client.on('end', () => {
//         console.log('disconnected from server');
//     });
// }

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;
    document.getElementById("battery").innerHTML+=1;
    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        // key_client('87');
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        // key_client('83');
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        // key_client('65');
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        // key_client('68');
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;
    document.getElementById("battery").innerHTML=Number(0);
    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}

// setInterval(function(){
//     // get image from python server
//     client();
// }, 1000);

function test(){
    document.getElementById("battery").innerHTML=Number(document.getElementById("battery").innerHTML)+1;
}

function client(msggg)
{
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${msggg}`);
        test();
        // document.getElementById("sign").innerHTML = mmss;
    });
    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function update_data(){
    if (document.getElementById("stream").value == "ON") {
        document.getElementById("stream").innerHTML = "end";
        document.getElementById("stream").value = "OFF";
        client("end");
    } else {
        document.getElementById("stream").innerHTML = "start";
        document.getElementById("stream").value = "ON";
        client("start");  
    }
}

// // update data for every 50ms
// function update_data(){
//     console.log('update_data');
//     if (document.getElementById("update").value == "ON") {

//         document.getElementById("update").value = "OFF"
//         clearInterval(flag)
//         document.getElementById("battery").innerHTML = 0;
//     } else {
//         // document.getElementById("battery").innerHTML = "2";
//         document.getElementById("update").value = "ON"
//         flag=setInterval(function(){test();}, 1000);
//     }
    
//     // document.getElementById("battery").innerHTML = "1";
//     // setInterval(function(){
//     //     // get image from python server
//     //     client();
//     // }, 1000);
// }

