$(document).ready(function() {

    $('#calendar').fullCalendar({
        events: '/calendar_feed',

        eventClick: function(calEvent, jsEvent, view) {
            $.getJSON('/calendar_feed',
                {
                    workout_id: calEvent.id
                },
                function(data) {
                    alert(data.units + ' ' + data.uom); 
                });
        }

    })

});