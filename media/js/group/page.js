if ((app.key == "meeting" && (app.page == "journal_club" || app.page == "youtube" || app.page == "rotation")) || (app.key == "res" && app.page == "archive")) {
    var toggle_flag = false;
    $("#btn_toggle").on("click", function() {
        if (toggle_flag) {
            $("#toggle_table").fadeIn(250);
            $("#toggle_timeline").fadeOut(250);
            $("#label_table").css({"font-weight":"bold", "text-decoration":"underline", 'color': '#29be92'});
            $("#label_timeline").css({"font-weight":"normal", "text-decoration":"none", 'color': '#000'});
        } else {
            $("#toggle_table").fadeOut(250);
            $("#toggle_timeline").fadeIn(250);
            $("#label_table").css({"font-weight":"normal", "text-decoration":"none", 'color': '#000'});
            $("#label_timeline").css({"font-weight":"bold", "text-decoration":"underline", 'color': '#29be92'});
        }
        toggle_flag = !toggle_flag;
    });
    $("#btn_toggle").trigger("click");

} else if (app.key == "meeting") {
    if (app.page == "schedule") {
        $("#iframe").css("width", parseInt($("#content").css("width")) - 50);
    } else if (app.page == "flash_slide") {
        $("#flash_list > div.subpanel:first > div.panel-collapse").collapse("show");

        $('div.panel-collapse').on('shown.bs.collapse', function() {
            $(this).prev().children().first().removeClass("glyphicon-chevron-left").addClass("glyphicon-chevron-down");
            $(this).prev().css("color", "#555");

            $(this).children().each(function() {
                var max_height = 0, row = $(this);
                row.children().each(function() {
                    var well = $(this).children().children().last();
                    if (parseInt(well.css("height")) > max_height) { max_height = parseInt(well.css("height")); }
                });
                row.children().each(function() {
                    var well = $(this).children().children().last();
                    well.css("height", max_height.toString() + "px");
                });
            });
        });
        $('div.panel-collapse').on('hidden.bs.collapse', function() {
            $(this).prev().children().first().removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-left");
            $(this).prev().css("color", "#ddd");
        });
    }

} else if (app.key == "calendar") {
    if (app.isCDN) {
        var cal_js = [
            'https://cdnjs.cloudflare.com/ajax/libs/moment.js/' + app.js_ver.moment + '/moment.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/' + app.js_ver.fullcal + '/fullcalendar.min.js'
        ];
    } else {
        var cal_js = [
            '/site_media/js/moment.min.js',
            '/site_media/js/fullcalendar.min.js'
        ];
    }
    cal_js = cal_js.concat(['/site_media/css/fullcalendar.min.css']);
    head.test($.fullCalendar, [], cal_js, function(flag) {
        $.ajax({
            url : "/group/gcal_dash/",
            dataType: "json",
            success : function (data) {
                $('#calendar').fullCalendar({
                    events: data,
                    timeFormat: ' h:mmt \n'
                });
                $("#calendar").removeClass("place_holder");
    
                $(".fc-today").css({"background-color": "#000", "color": "#fef159", "font-weight": "bold"});
                $("th.fc-day-header").css({"background-color": "#ddd", "padding": "10px"});
                $("button.fc-prev-button").removeClass("fc-button fc-state-default fc-corner-left fc-corner-right").addClass("btn btn-blue").html('<span class="glyphicon glyphicon-backward"></span>&nbsp;');
                $("button.fc-next-button").removeClass("fc-button fc-state-default fc-corner-left fc-corner-right").addClass("btn btn-blue").html('&nbsp;<span class="glyphicon glyphicon-forward"></span>');
                $("button.fc-today-button").removeClass("fc-button fc-state-default fc-corner-left fc-corner-right").addClass("btn btn-inverse").html('<span class="glyphicon glyphicon-map-marker"></span>&nbsp;&nbspToday');

                $(".fc-prev-button, .fc-next-button, .fc-today-button").bind("click", function() {
                    $(".fc-today").css({"background-color": "#000", "color": "#fef159", "font-weight": "bold"});
                    $("th.fc-day-header").css({"background-color": "#ddd", "padding": "10px"});
                });
            }
        });
    });

} else if (app.key == "res") {
    if (app.page == "gdocs") {
    } else if (app.page == "archive") {
    } else if (app.page == "contact") {
        var max_height = 0;
        $("div.profile-card").each(function () {
            if (parseInt($(this).css("height")) > max_height) { max_height = parseInt($(this).css("height")); }
        }); 
        $("div.profile-card").each(function () {
            $(this).css("height", max_height.toString() + "px");
        }); 

        var toggle_flag = false;
        $("#btn_toggle").on("click", function () {
            if (toggle_flag) {
                $("#toggle_table").fadeIn(250);
                $("#toggle_card").fadeOut(250);
                $("#label_table").css({"font-weight":"bold", "text-decoration":"underline"});
                $("#label_card").css({"font-weight":"normal", "text-decoration":"none"});
            } else {
                $("#toggle_table").fadeOut(250);
                $("#toggle_card").fadeIn(250);
                $("#label_table").css({"font-weight":"normal", "text-decoration":"none"});
                $("#label_card").css({"font-weight":"bold", "text-decoration":"underline"});
            }
            toggle_flag = !toggle_flag;
        });
        $("#btn_toggle").trigger("click");
        $("img").css("max-width", "100%");
    }
} else if (app.key == "server") {
    if (app.page == "aws") {
        $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'aws' + app.DEBUG_STR + '.js', function() {
            $("[id^=aws_]").on('click', function() {
                $('html, body').stop().animate({scrollTop: $($(this).attr("href")).offset().top - 75}, 500);
            });
        });
    } else if (app.page == "ga") {
        $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'ga' + app.DEBUG_STR + '.js');
    }
} else if (app.key == "service") {
    if (app.page == "bot") {
        $.getScript('/site_media/css/fullcalendar.min.css');
    } else if (app.page == "git") {
        $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'git' + app.DEBUG_STR + '.js');
    } else if (app.page == "slack") {
        $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'slack' + app.DEBUG_STR + '.js');
    } else if (app.page == "dropbox") {
        $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'dropbox' + app.DEBUG_STR + '.js');
    }
} else if (app.key == "misc") {
    if (app.page == "error") {
        $("#iframe").css("width", parseInt($("#content").css("width")) - 50);
        $("input:radio").on("change", function() {
            $("#iframe").attr("src", "/error/" + $(this).val() + '/?status=false');
        });
    }
} else if (app.key == "home") {
    $("#banner_div").on("click", function(event) {
        $("#baking-modal").modal("show");
        event.preventDefault();
    });
    $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'home' + app.DEBUG_STR + '.js');
    if (app.DEBUG_DIR) {
        $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'clock' + app.DEBUG_STR + '.js');
    }
}

