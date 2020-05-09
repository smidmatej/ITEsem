var value = document.querySelector('.value')
value.textContent = 'PES';
    websocket = new WebSocket("ws://127.0.0.1:6789/");
            websocket.onmessage = function (event) {
                data = JSON.parse(event.data);
                switch (data.type) {
                    case 'state':
                        value.textContent = data.value;
                        break;
                    default:
                        console.error(
                            "unsupported event", data);
                }
            }; 
