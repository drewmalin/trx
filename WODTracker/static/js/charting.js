$(function () {
    var chart;
    var workoutList = [];
    var dateList = [];
    var series = [];
    var units;
    var name;
    var str;

    $(document).ready(function() {
      
      // Initial chart generation, happens upon page load
      requestData();

      /*
       * Request data from the server
       */
      function requestData() {
        // Re-generate chart when a new exercise is selected
        $("#refresh_button").click(function() {
          //requestData();
          $.getJSON('/workouts/' + '?exercises=' + $("#exerciseDropdown").val() + '&users=' + $("#userDropdown").val(),
              function(data) {
                if (data != null) {
                  dateList = data.dates;
                  units = data.units;
                  name = data.exercise;
                  series = data.data;
                }
                generateChart(data);
              }
            );
        })}
        /* OLD CODE BELOW! 
        $.getJSON('/users/'+$("#chart").attr("uid")+'/exercises/'+$("#refresh_list").val()+'/',
          function(data) {
            if (data != null) {
              workoutList = [];
              dateList = [];
              
              units = data[0].uom;
              name = data[0].exercise_name;

              for (var i = 0; i < data.length; i++) {
                workoutList[i] = parseInt(data[i].units);
                dateList[i] = data[i].date;
              }
            }
            generateChart(data);
          }
        );
      }
      */

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
              text: name,
              x: -20 //center
          },
          xAxis: {
              categories: dateList
          },
          yAxis: {
              title: {
                  text: units
              },
              plotLines: [{
                  value: 0,
                  width: 1,
                  color: '#808080'
              }]
          },
          tooltip: {
              formatter: function() {
                      return '<b>'+ name +'</b><br/>'+
                      this.x +': '+ this.y +' '+ units;
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
          series: series
        });
      }
    });    
});