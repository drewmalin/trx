$(document).ready(function() {

    $('#calendar').fullCalendar({
        events: 'http://127.0.0.1:5000/_request_calendar',

    	eventClick: function(calEvent, jsEvent, view) {
    		$.getJSON('http://127.0.0.1:5000/_request_workout', 
          	{
            	workoutID: calEvent.id
          	},
          	function(data) {
            	alert(data.units + ' ' + data.uom);	
          	});
    	}

    })

});