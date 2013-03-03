$(document).ready(function() {
    $('#calendar').fullCalendar({
        events: '/calendar_feed',
        eventClick: function(calEvent, jsEvent, view) {
            $.getJSON('/users/'+$("#calendar").attr("uid")+'/workouts/'+calEvent.id+'/',

            function(data) {
                if (data == null) return;
                //calendarEventModal.toggle();
                $('#calendarEvent #myModalLabel').text(data[0].exercise_name + ' -- ' + data[0].date);
                $('#calendarEvent #modal-body').html(data[0].units + ' ' + data[0].uom + '<br>' + data[0].extra_credit);
                $('#calendarEvent').modal({
                    keyboard:false
                });
            });
        }
    });
});
