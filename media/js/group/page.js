if ((app.key == "meeting" && (app.page == "journal_club" || app.page == "eterna_youtube" || app.page == "rotation")) || (app.key == "res" && (app.page == "archive" || app.page == "defense"))) {
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
        if (app.DEBUG_DIR) {
            var cal_js = ['/site_media/js/public/min/cal.min.js'];
        } else {
            var cal_js = [
                '/site_media/js/moment.min.js',
                '/site_media/js/fullcalendar.min.js'
            ];
        }
    }
    cal_js = cal_js.concat(['/site_media/css/fullcalendar.min.css']);
    head.test($.fullCalendar, [], cal_js, function(flag) {
        $.ajax({
            url : "/group/dash/gcal/",
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
    if (app.page == "archive/upload") {
        $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'upload' + app.DEBUG_STR + '.js');
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

        $("#id_contact_email").prop("disabled", true);
        $("#id_contact_phone").prop("disabled", true);
        $("#id_contact_bday").prop("disabled", true);
        $("#form_change_submit").prop("disabled", true);
        var user_dash_timeout = setTimeout(function() {
            if (app.user !== undefined) {
                clearTimeout(user_dash_timeout);

                var photo_html = '';
                if (app.user.photo) {
                    photo_html = app.user.photo;
                } else {
                    photo_html = '<img src="/site_media/images/icon_default_avatar.png" width="119">';
                }
                if (app.user.type === 'admin') { photo_html += '<p><span class="label label-magenta"><span class="glyphicon glyphicon-king" aria-hidden="true"></span>&nbsp;&nbsp;Administrator</span></p>'; }
                $("#card_user_photo").html(photo_html);
                $("#card_user_photo > img").css("max-width", "100%");
                $("#card_user_name").html(app.user.name);
                $("#card_user_id").html(app.user.id);
                $("#card_user_aff").html(app.user.title);
                $("#card_user_stat").html(app.user.status);
                $("#card_user_cap").attr("href", app.user.cap);
                if (app.user.email) {
                    $("#card_user_email").html(app.user.email);
                    $("#card_user_email").attr("href", "mailto:" + app.user.email);
                    $("#id_contact_email").val(app.user.email);
                }
                if (app.user.phone) {
                    $("#card_user_phone").html(app.user.phone);
                    $("#id_contact_phone").val(app.user.phone.replace(/\D+/g, ''));
                }
                if (app.user.bday) { $("#id_contact_bday").val(app.user.bday); }
                if (app.user.type == 'admin' || app.user.type == 'group' || app.user.type == 'alumni') {
                    $("#id_contact_email").prop("disabled", false);
                    $("#id_contact_phone").prop("disabled", false);
                    $("#id_contact_bday").prop("disabled", false);
                    $("#form_change_submit").prop("disabled", false);
                }
            }
        }, 500);
    }
} else if (app.key == "server" && app.page == "aws") {
    $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'gapi' + app.DEBUG_STR + '.js', function() {
        $("[id^=aws_]").on('click', function() {
            $('html, body').stop().animate({scrollTop: $($(this).attr("href")).offset().top - 75}, 500);
        });
    });
} else if ((app.key == "server" && app.page == "ga") || (app.key == "service" && (app.page == "git" || app.page == "slack" || app.page == "dropbox"))) {
    $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'gapi' + app.DEBUG_STR + '.js');
} else if (app.key == "service" && app.page == "bot") {
    head.load('/site_media/css/fullcalendar.min.css');
} else if (app.key == "misc") {
    if (app.page == "error") {
        $("#iframe").css("width", parseInt($("#content").css("width")) - 50);
        $("input:radio").on("change", function() {
            $("#iframe").attr("src", "/error/" + $(this).val() + '/?status=false');
        });
    }
} else if (app.key == "home") {
    head.load('/site_media/css/' + app.DEBUG_DIR + 'clock' + app.DEBUG_STR + '.css');
    $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'home' + app.DEBUG_STR + '.js');
    if (!app.DEBUG_DIR) {
        $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'clock' + app.DEBUG_STR + '.js');
    }
    $("#banner_div").on("click", function(event) {
        $("#baking-modal").modal("show");
        event.preventDefault();
    });
}

