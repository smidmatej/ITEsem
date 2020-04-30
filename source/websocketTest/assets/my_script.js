function onBodyLoad() {
    ws = new WebSocket('ws://localhost:8881/websocket')     // ws is a global variable (my_page_ws.html)
    ws.onopen = onSocketOpen
    ws.onmessage = onSocketMessage
    ws.onclose = onSocketClose
}

function onSocketOpen() {
    console.log("WS client: Websocket opened.")
}

function onSocketMessage(message) {
    var data
    try {
        data = JSON.parse(message.data)    
    } catch(e) {
        data = message.data
    }
    console.log("WS message:", data)
    document.getElementById("ws_server_message").innerHTML = "Last message from server: "+data
}

function onSocketClose() {
    console.log("WS client: Websocket closed.")
}

function sendToServer() {
    var params = {
        name: "bob",
        subjects: ["apk", "ite"]
    }
    ws.send(JSON.stringify(params))
}