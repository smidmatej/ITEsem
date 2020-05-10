var blue_status = document.querySelector('.blue_stat')
var blue_cur_temp = document.querySelector('.blue_cur')
var blue_min_temp = document.querySelector('.blue_min')
var blue_max_temp = document.querySelector('.blue_max')
var blue_avg_temp = document.querySelector('.blue_avg')

var orange_status = document.querySelector('.orange_stat')
var orange_cur_temp = document.querySelector('.orange_cur')
var orange_min_temp = document.querySelector('.orange_min')
var orange_max_temp = document.querySelector('.orange_max')
var orange_avg_temp = document.querySelector('.orange_avg')

var red_status = document.querySelector('.red_stat')
var red_cur_temp = document.querySelector('.red_cur')
var red_min_temp = document.querySelector('.red_min')
var red_max_temp = document.querySelector('.red_max')
var red_avg_temp = document.querySelector('.red_avg')

var black_status = document.querySelector('.black_stat')
var black_cur_temp = document.querySelector('.black_cur')
var black_min_temp = document.querySelector('.black_min')
var black_max_temp = document.querySelector('.black_max')
var black_avg_temp = document.querySelector('.black_avg')

var yellow_status = document.querySelector('.yellow_stat')
var yellow_cur_temp = document.querySelector('.yellow_cur')
var yellow_min_temp = document.querySelector('.yellow_min')
var yellow_max_temp = document.querySelector('.yellow_max')
var yellow_avg_temp = document.querySelector('.yellow_avg')

var green_status = document.querySelector('.green_stat')
var green_cur_temp = document.querySelector('.green_cur')
var green_min_temp = document.querySelector('.green_min')
var green_max_temp = document.querySelector('.green_max')
var green_avg_temp = document.querySelector('.green_avg')

var pink_status = document.querySelector('.pink_stat')
var pink_cur_temp = document.querySelector('.pink_cur')
var pink_min_temp = document.querySelector('.pink_min')
var pink_max_temp = document.querySelector('.pink_max')
var pink_avg_temp = document.querySelector('.pink_avg')

websocket = new WebSocket("ws://127.0.0.1:6789/");
            websocket.onmessage = function (event) {
                data = JSON.parse(event.data);
                switch (data.Team) {
                    case 'blue':
                        blue_status.textContent = data.Status;
                        blue_cur_temp.textContent = data.cur_temp;
                        blue_min_temp.textContent = data.min_temp;
                        blue_max_temp.textContent = data.max_temp;
                        blue_avg_temp.textContent = data.avg_temp;
                        break;
                    case 'red':
                    	red_status.textContent = data.Status;
                        red_cur_temp.textContent = data.cur_temp;
                        red_min_temp.textContent = data.min_temp;
                        red_max_temp.textContent = data.max_temp;
                        red_avg_temp.textContent = data.avg_temp;
                        break;
                    case 'black':
                    	black_status.textContent = data.Status;
                        black_cur_temp.textContent = data.cur_temp;
                        black_min_temp.textContent = data.min_temp;
                        black_max_temp.textContent = data.max_temp;
                        black_avg_temp.textContent = data.avg_temp;
                        break;
                    case 'orange':
                    	orange_status.textContent = data.Status;
                        orange_cur_temp.textContent = data.cur_temp;
                        orange_min_temp.textContent = data.min_temp;
                        orange_max_temp.textContent = data.max_temp;
                        orange_avg_temp.textContent = data.avg_temp;
                        break;
                    case 'green':
                    	green_status.textContent = data.Status;
                        green_cur_temp.textContent = data.cur_temp;
                        green_min_temp.textContent = data.min_temp;
                        green_max_temp.textContent = data.max_temp;
                        green_avg_temp.textContent = data.avg_temp;
                        break;
                    case 'pink':
                    	pink_status.textContent = data.Status;
                        pink_cur_temp.textContent = data.cur_temp;
                        pink_min_temp.textContent = data.min_temp;
                        pink_max_temp.textContent = data.max_temp;
                        pink_avg_temp.textContent = data.avg_temp;
                        break;
                    case 'yellow':
                    	yellow_status.textContent = data.Status;
                        yellow_cur_temp.textContent = data.cur_temp;
                        yellow_min_temp.textContent = data.min_temp;
                        yellow_max_temp.textContent = data.max_temp;
                        yellow_avg_temp.textContent = data.avg_temp;
                        break;
                    default:
                        console.error(
                            "unsupported event", data);
                }
            };

