if ("WebSocket" in window) {
    var rname = document.getElementById("roomname").innerHTML;
    var ws = new WebSocket("ws://" + location.host + "/chatting?name="+ rname);
    ws.onopen = function () {
        var x = document.getElementById("content");
        if (localStorage.getItem(rname) == null) { //bug  todo 
            x.innerHTML = "欢迎加入聊天室!"
        }
        else {
            x.innerHTML = localStorage.getItem(rname);
        }
    }
    ws.onmessage = function (evt) {
        var msg = evt.data;
        var x = document.getElementById("content");
        if (config_cmd(msg) == true) {
            sys_call(msg);
        }
        else {
            if(x.innerHTML != ""){
                x.innerHTML = x.innerHTML + "\r\n" + msg;
                x.scrollTop = x.scrollHeight; //刷新消息，显示最后一行
            }
            else{
                x.innerHTML = msg;
                x.scrollTop = x.scrollHeight; //刷新消息，显示最后一行
            }
            
        }
    }
    ws.onclose = function () {
        alert("已与服务器断开连接...");
        history();
    }
}
else {
    alert("您的浏览器不支持websocket!");
}

function wsSend() {
    var msg = document.getElementById("msg");
    if (msg.value == "") {
        alert("请不要发送空消息！");
    }
    else {
        var name = document.getElementById("username");
        ws.send(name.innerHTML + ":" + msg.value);
        msg.value = "";
    }

}

function history() {
    if (typeof (Storage) != "undefined") {
        var rname = document.getElementById("roomname").innerHTML;
        localStorage.setItem(rname, document.getElementById("content").innerHTML);
    }
    else {
        alert("不支持本地缓存!");
    }
}

function clean() {
    localStorage.clear();
    document.getElementById("content").innerHTML = "";
}

function keyDown(event) {
    if (event.keyCode == 13) {
        wsSend();
    }
}

function flush() {
    history();
    var rname = document.getElementById("roomname").innerHTML;
    document.getElementById("content").innerHTML = localStorage.getItem(rname);
    location.reload(true); //解决bug界面卡死问题
}

function re_users() {
    //null
}

function sys_call(msg) {//本功能仅供娱乐
    cmd = msg.split(":")[1].slice(13);
    if (cmd == "clear") {
        clean();
    }
    else {
        alert("请输入有效命令(来自管理员的凝视)")
    }
}

function config_cmd(msg) {
    if (msg.split(":")[1].substring(0, 12) == "/System Call")
        return true;
    else
        return false;
}
