
                document.querySelector('.textBox').textContent = '2'

websocket = new WebSocket("ws://" + window.location.hostname + ":6789/");
websocket.onmessage = function (event) {
    message = JSON.parse(event.data);
    data = message.HISTORY
    document.querySelector('.textBox').textContent = message.HISTORY.blue.x

               
                
                

    var blueChart = document.getElementById('blueChart').getContext('2d');
    var blueDatachart = new Chart(blueChart, {
        // The type of chart we want to create
        type: 'line', //chart type

        // The data for our dataset
        data: {
            labels: message.HISTORY.blue.x, //x values
            datasets: [{
                label: 'My First dataset',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: message.HISTORY.blue.y //y values
                }]
            },
        options: {}
    });

    var blackChart = document.getElementById('blackChart').getContext('2d');
    var blackDatachart = new Chart(blackChart, {
        // The type of chart we want to create
        type: 'line', //chart type

        // The data for our dataset
        data: {
            labels: message.HISTORY.black.x, //x values
            datasets: [{
                label: 'My First dataset',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: message.HISTORY.black.y //y values
                }]
            },
        options: {}
    });
    
     var greenChart = document.getElementById('greenChart').getContext('2d');
    var greenDatachart = new Chart(greenChart, {
        // The type of chart we want to create
        type: 'line', //chart type

        // The data for our dataset
        data: {
            labels: message.HISTORY.green.x, //x values
            datasets: [{
                label: 'My First dataset',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: message.HISTORY.green.y //y values
                }]
            },
        options: {}
    });
    
     var orangeChart = document.getElementById('orangeChart').getContext('2d');
    var orangeDatachart = new Chart(orangeChart, {
        // The type of chart we want to create
        type: 'line', //chart type

        // The data for our dataset
       data: {
            labels: message.HISTORY.orange.x, //x values
            datasets: [{
                label: 'My First dataset',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: message.HISTORY.orange.y //y values
                }]
            },
        options: {}
    });
    
     var pinkChart = document.getElementById('pinkChart').getContext('2d');
    var pinkDatachart = new Chart(pinkChart, {
        // The type of chart we want to create
        type: 'line', //chart type

        // The data for our dataset
        data: {
            labels: message.HISTORY.pink.x, //x values
            datasets: [{
                label: 'My First dataset',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: message.HISTORY.pink.y //y values
                }]
            },
        options: {}
    });
    
     var redChart = document.getElementById('redChart').getContext('2d');
    var redDatachart = new Chart(redChart, {
        // The type of chart we want to create
        type: 'line', //chart type

        // The data for our dataset
        data: {
            labels: message.HISTORY.red.x, //x values
            datasets: [{
                label: 'My First dataset',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: message.HISTORY.red.y //y values
                }]
            },
        options: {}
    });
    
     var yellowChart = document.getElementById('yellowChart').getContext('2d');
    var yellowChart = new Chart(yellowChart, {
        // The type of chart we want to create
        type: 'line', //chart type

        // The data for our dataset
        data: {
            labels: message.HISTORY.yellow.x, //x values
            datasets: [{
                label: 'My First dataset',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: message.HISTORY.yellow.y //y values
                }]
            },
        options: {}
    });
    
}
