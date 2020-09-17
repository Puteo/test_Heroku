$(window).on("load", init());

function init() {
    $("#button").click(function() {
        var textData = JSON.stringify({ "message": $("#message").val() });
        $.ajax({
            type: 'POST',
            url: '/message',
            data: textData,
            contentType: 'application/json',
            success: function(data) {
                $("#message").val("");
            }
        });
    });

    $("#clearbutton").click(function() {
        $("#log").empty()
        $.ajax({
            type: 'POST',
            url: '/Delete_message',
        });
    });

    $("#logout").click(function() {
        $.ajax({
            type: 'POST',
            url: '/logout',
        });
    });

    var showmessage = function() {
        $.ajax({
            type: 'GET',
            url: '/message',
            contentType: 'application/json',
            success: function(data) {

                var name = JSON.parse(data.ResultSet).name;
                var message = JSON.parse(data.ResultSet).message;
                var time = JSON.parse(data.ResultSet).str_time;
                var n = Object.keys(name).length;
                var logdata = "";
                if (n != 0) {
                    for (var i = 0; i < n; i++) {
                        logdata = logdata + "<h3>" + time[i] + "   :   " + name[i] + " wrote : " + message[i] + "</h3>" + "\r\n"
                    }
                    $("#log").html(logdata)
                }
            }
        });
    }
    setInterval(showmessage, 1000 * 10);
}