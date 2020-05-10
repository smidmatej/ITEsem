var dict = {
	Team : "",
	Status : "",
	cur_temp : 0,
	min_temp : 0,
	max_temp : 0,
	avg_temp : 0
};

var blue_status = document.querySelector('.blue_stat')
var blue_cur_temp = document.querySelector('.blue_cur')
var blue_min_temp = document.querySelector('.blue_min')
var blue_max_temp = document.querySelector('.blue_max')
var blue_avg_temp = document.querySelector('.blue_avg')

var orange_dict = {};
var red_dict = {};
var black_dict = {};
var yellow_dict = {};
var green_dict = {};
var pink_dict = {};


websocket = new WebSocket("ws://127.0.0.1:6789/");
            websocket.onmessage = function (event) {
                data = JSON.parse(event.data);
                switch (data.type) {
                    case 'Team':
                        dict.Team = data.value;
                    case 'Status':
                    	dict.Status = data.value;
                    case 'cur_temp':
                    	dict.cur_temp = data.value;
                    case 'min_temp':
                    	dict.min_temp = data.value;
                    case 'max_temp':
                    	dict.max_temp = data.value;
                    case 'avg_temp':
                    	dict.avg_temp = data.value;
                    default:
                        console.error(
                            "unsupported event", data);
                }
            };

if (dict[Team] == 'blue'){
	blue_status.textContent = dict[Status];
	blue_cur_temp.textContent = dict[cur_temp];
	blue_min_temp.textContent = dict[min_temp];
	blue_max_temp.textContent = dict[max_temp];
	blue_avg_temp.textContent = dict[avg_temp];
}else if (dict[Team] == 'orange'){
	orange_dict = dict
}else if (dict[Team] == 'red'){
	red_dict = dict
}else if (dict[Team] == 'black'){
	black_dict = dict
}else if (dict[Team] == 'yellow'){
	yellow_dict = dict
}else if (dict[Team] == 'green'){
	green_dict = dict
}else if (dict[Team] == 'pink'){
	pink_dict = dict
}

