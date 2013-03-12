$(function () {
    var chart;
    var workoutList = [];
    var dateList = [];
    var series = [];
    var units;
    var name;
    var str;

    $(document).ready(function() {
      
        $("#select-workout").select2({
            placeholder: "Select a workout",
            ajax: {
                url: "/exercisedropdown/",
                dataType: "json",
                data: function(term, page) {
                    return { q: term, page: page, per: 10 };
                },
                results: function(data, page) {
                    return { results: data.results };
                }
            }
        });

        $("#select-user").select2({
            placeholder: "Select users",
            multiple: "true",
            ajax: {
                url: "/userdropdown/",
                dataType: "json",
                data: function(term, page) {
                    return { q: term, page: page, per: 10 };
                },
                results: function(data, page) {
                    return { results: data.results };
                }
            }
        });

        var now = new Date();
        now.setHours(0);
        now.setMinutes(0);
        now.setSeconds(0);

        var datefrom = $("#date-from")
            .datepicker()
            .on('show', function(ev) {
                if (ev.date.valueOf() < now.valueOf()) {
                    return 'disabled';
                }
                else {
                    return '';
                }
            })
            .on('changeDate', function(ev) {
                if (ev.date.valueOf() > dateto.date.valueOf()) {
                    var newDate = new Date(ev.date);
                    newDate.setDate(newDate.getDate() + 1);
                    dateto.setValue(newDate);
                }
                datefrom.hide();
            })
            .data('datepicker');

        var dateto = $("#date-to").datepicker({
            onRender: function(date) {
                if (date.valueOf() > now.valueOf() ||
                    date.valueOf() <= datefrom.date.valueOf()) {
                    return 'disabled';
                }
                else {
                    return '';
                }
            }
        }).on('changeDate', function(chEvent) {
            dateto.hide();
        }).data('datepicker');
      // Initial chart generation, happens upon page load
      requestData();

      /*
       * Request data from the server
       */
      function requestData() {
        // Re-generate chart when a new exercise is selected
        $("#refresh_button").click(function() {
          //requestData();
          $.getJSON('/workouts/' + '?exercises=' + $("#select-workout").val() + '&users=' + $("#select-user").val(),
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
