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

//websocket = new WebSocket("ws://127.0.0.1:6789/");
websocket = new WebSocket("ws://" + window.location.hostname + ":6789/");
blue_status.textContent = "ws://" + window.location.hostname + ":6789/";
            websocket.onmessage = function (event) {
                message = JSON.parse(event.data);
                    data = message.STATE
                
                        blue_status.textContent = data.blue.Status;
                        blue_cur_temp.textContent = data.blue.cur_temp;
                        blue_min_temp.textContent = data.blue.min_temp;
                        blue_max_temp.textContent = data.blue.max_temp;
                        blue_avg_temp.textContent = data.blue.avg_temp;
                        
                    	

                    	black_status.textContent = data.black.Status;
                        black_cur_temp.textContent = data.black.cur_temp;
                        black_min_temp.textContent = data.black.min_temp;
                        black_max_temp.textContent = data.black.max_temp;
                        black_avg_temp.textContent = data.black.avg_temp;
                        
                        green_status.textContent = data.green.Status;
                        green_cur_temp.textContent = data.green.cur_temp;
                        green_min_temp.textContent = data.green.min_temp;
                        green_max_temp.textContent = data.green.max_temp;
                        green_avg_temp.textContent = data.green.avg_temp;
                        
                        orange_status.textContent = data.orange.Status;
                        orange_cur_temp.textContent = data.orange.cur_temp;
                        orange_min_temp.textContent = data.orange.min_temp;
                        orange_max_temp.textContent = data.orange.max_temp;
                        orange_avg_temp.textContent = data.orange.avg_temp;
                        
                        pink_status.textContent = data.pink.Status;
                        pink_cur_temp.textContent = data.pink.cur_temp;
                        pink_min_temp.textContent = data.pink.min_temp;
                        pink_max_temp.textContent = data.pink.max_temp;
                        pink_avg_temp.textContent = data.pink.avg_temp;
                        
                        red_status.textContent = data.red.Status;
                        red_cur_temp.textContent = data.red.cur_temp;
                        red_max_temp.textContent = data.red.max_temp;
                        red_min_temp.textContent = data.red.min_temp;
                        red_avg_temp.textContent = data.red.avg_temp;
                        
                        yellow_status.textContent = data.yellow.Status;
                        yellow_cur_temp.textContent = data.yellow.cur_temp;
                        yellow_min_temp.textContent = data.yellow.min_temp;
                        yellow_max_temp.textContent = data.yellow.max_temp;
                        yellow_avg_temp.textContent = data.yellow.avg_temp;

                
            };

