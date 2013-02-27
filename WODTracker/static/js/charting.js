$(function () {
    var chart;
    var workoutList = [];
    var dateList = [];

    var str;
    $(document).ready(function() {
      
      // Initial chart generation, happens upon page load
      requestData();

      // Re-generate chart when a new exercise is selected
      $("#refresh_button").click(function() {
        requestData();
      });   

      /*
       * Request data from the server
       */
      function requestData() {
        $.getJSON('http://127.0.0.1:5000/_request_workouts', 
          {
            exercise: $("#refresh_list").val()
          },
          function(data) {
            workoutList = [];
            dateList = [];

            for (var i = 0; i < data.arr.length; i++) {
              workoutList[i] = parseInt(data.arr[i]);
            }
            for (var i = 0; i < data.dates.length; i++) {
              dateList[i] = data.dates[i];
            }
            
            generateChart(data);
          }
        );
      }

      /*
       * Generate chart using Highchart
       */
      function generateChart(data) {
        chart = new Highcharts.Chart({
          chart: {
              renderTo: 'chart',
              type: 'line',
              marginRight: 130,
              marginBottom: 25
          },
          title: {
              text: data.name,
              x: -20 //center
          },
          xAxis: {
              categories: dateList
          },
          yAxis: {
              title: {
                  text: data.units
              },
              plotLines: [{
                  value: 0,
                  width: 1,
                  color: '#808080'
              }]
          },
          tooltip: {
              formatter: function() {
                      return '<b>'+ this.series.name +'</b><br/>'+
                      this.x +': '+ this.y +' '+ data.units;
              }
          },
          legend: {
              layout: 'vertical',
              align: 'right',
              verticalAlign: 'top',
              x: -10,
              y: 100,
              borderWidth: 0
          },
          series: [{
              name: data.name,
              data: workoutList
          }]
        });
      }
    });    
});
/*
              <ul class="nav nav-pills">
                <li class="active">
                  <a href="{{ url_for('index') }}">Home</a>
                </li>
              </ul>
              */