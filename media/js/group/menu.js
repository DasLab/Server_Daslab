var side_toggle = true;
var throttle = function(func, delay, at_least) {
  var timer = null, previous = null;
  return function() {
    var now = +new Date();
    if (!previous) { previous = now; }
    if (now - previous > at_least) {
      func();
      previous = now;
    } else {
      clearTimeout(timer);
      timer = setTimeout(func, delay);
    }
  };
};

app.fnParseLocation = function() {
    var urls = {
        "meeting": ["schedule", "flash_slide", "journal_club", "eterna_youtube", "rotation"],
        "calendar": ["calendar"],
        "res": ["gdocs", "archive", "archive/upload", "defense", "contact"],
        "server": ["aws", "ga"],
        "service": ["bot", "secret", "git", "slack", "dropbox"],
        "misc": ["misc", "error"]
    };
    app.page = window.location.pathname.replace('/group', '').replace(/\/$/, '').replace(/^\//, '');
    for (var key in urls) {
        if (urls[key].indexOf(app.page) != -1) {
            app.key = key;
            return;
        }
    }
    app.key = 'home';
};

app.fnChangeBreadcrumb = function() {
    $("ul.breadcrumb li:not(:first-child)").remove();
    if (app.key == "meeting") {
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff5c2b");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-bell"></span>&nbsp;&nbsp;<a href="">Group Meeting</a></li>').insertAfter($("ul.breadcrumb > li:first"));

        if (app.page == "schedule") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;<a href="https://docs.google.com/spreadsheets/d/1GWOBc8rRhLNMEsf8pQMUXkqqgRiYTLo22t1eKP83p80/edit#gid=1" target="_blank" rel="noopener noreferrer external">Google Spreadsheet&nbsp;&nbsp;<span class="glyphicon glyphicon-new-window" style="font-size:14px;"></span></a></li>');
        } else if (app.page == "flash_slide") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-blackboard"></span>&nbsp;&nbsp;Flash Slides</li>');
        } else if (app.page == "journal_club") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-book"></span>&nbsp;&nbsp;Journal Club Presentations</li>');
        } else if (app.page == "eterna_youtube") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-facetime-video"></span>&nbsp;&nbsp;<a href="https://www.youtube.com/channel/UCt811OXJqe35TDhe9hPYzJg/" target="_blank" rel="noopener noreferrer external">Eterna Dev <span class="label" style="color:#000;">You</span><span class="label label-danger">Tube</span> Channel&nbsp;&nbsp;<span class="glyphicon glyphicon-new-window" style="font-size:14px;"></span></a></li>');
        } else if (app.page == "rotation") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-retweet"></span>&nbsp;&nbsp;Rotation Student Presentations</li>');
        }
    } else if (app.key == "calendar") {
        $("ul.breadcrumb").css("border-bottom", "5px solid #c28fdd");
        $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;<a href="https://www.google.com/calendar/embed?src=a53lhn4i0fgrkcs9c6i85fdmdo%40group.calendar.google.com&ctz=America/Los_Angeles" target="_blank" rel="noopener noreferrer external">Google Calendar&nbsp;&nbsp;<span class="glyphicon glyphicon-new-window" style="font-size:14px;"></span></a></li>');
    } else if (app.key == "res") {
        $("ul.breadcrumb").css("border-bottom", "5px solid #eeb211");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-briefcase"></span>&nbsp;&nbsp;<a href="">Resources</a></li>').insertAfter($("ul.breadcrumb > li:first"));
        if (app.page == "gdocs") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_gdrive"></i></div>&nbsp;&nbsp;Google Documents</li>');
        } else if (app.page.startsWith("archive")) {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-cd"></span>&nbsp;&nbsp;Presentations Archive</li>');
            if (app.page == "archive/upload") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-open"></span>&nbsp;&nbsp;Upload</li>');
                $('#nav_res-archive').addClass("active");
            }
        } else if (app.page == "defense") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-scissors"></span>&nbsp;&nbsp;Defense Posters</li>');
        } else if (app.page == "contact") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-earphone"></span>&nbsp;&nbsp;Contacts</li>');
        }
    } else if (app.key == "server") {
        $("ul.breadcrumb").css("border-bottom", "5px solid #50cc32");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;<a href="">Servers</a></li>').insertAfter($("ul.breadcrumb > li:first"));
        if (app.page == "aws") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_aws"></i></div>&nbsp;&nbsp;Amazon Web Services</li>');
        } else if (app.page == "ga") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_ga"></i></div>&nbsp;&nbsp;Google Analytics</li>');
        }
    } else if (app.key == "service") {
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff912e");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;<a href="">Services</a></li>').insertAfter($("ul.breadcrumb > li:first"));
        if (app.page == "bot") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_bot"></i></div>&nbsp;&nbsp;DasLab Bot</li>');
        } else if (app.page == "secret") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-usd"></span>&nbsp;&nbsp;Shared Secrets</li>');
        } else if (app.page == "git") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_git"></i></div>&nbsp;&nbsp;<a href="https://www.github.com/DasLab/" target="_blank" rel="noopener noreferrer external">GitHub Repositories&nbsp;&nbsp;<span class="glyphicon glyphicon-new-window" style="font-size:14px;"></span></a></li>');
        } else if (app.page == "slack") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_slack"></i></div>&nbsp;&nbsp;<a href="https://das-lab.slack.com/" target="_blank" rel="noopener noreferrer external">Slack&nbsp;&nbsp;<span class="glyphicon glyphicon-new-window" style="font-size:14px;"></span></a></li>');
        } else if (app.page == "dropbox") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_dropbox"></i></div>&nbsp;&nbsp;<a href="https://www.dropbox.com/" target="_blank" rel="noopener noreferrer external">Dropbox&nbsp;&nbsp;<span class="glyphicon glyphicon-new-window" style="font-size:14px;"></span></a></li>');
        }
    } else if (app.key == "misc") {
        $("ul.breadcrumb").css("border-bottom", "5px solid #5496d7");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-magnet"></span>&nbsp;&nbsp;<a href="">Miscellaneous</a></li>').insertAfter($("ul.breadcrumb > li:first"));
        if (app.page == "misc") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-hand-right"></span>&nbsp;&nbsp;Onboarding Instructions</li>');
        } else if (app.page == "error") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-volume-off"></span>&nbsp;&nbsp;HTTP Error Pages</li>');
        }
    } else {
        $("ul.breadcrumb").css("border-bottom", "5px solid #3ed4e7");
    }
};

app.fnChangeView = function() {
    app.fnParseLocation();
    $("#sidebar-wrapper ul li.active").removeClass("active");
    $("#sidebar-wrapper a[href='" + window.location.pathname + "']").parent().addClass("active");
    $("#nav_" + app.key).addClass("active");
    $("#nav_" + app.key + "_lg").addClass("active");

    app.fnChangeBreadcrumb();
    $.getScript('/site_media/js/group/' + app.DEBUG_DIR + 'page' + app.DEBUG_STR + '.js', function(data, code, xhr) {
        $("#content").fadeTo(150, 1);
        if (window.location.hash) { $('html, body').stop().animate({"scrollTop": $(window.location.hash).offset().top - 75}, 500); }
        if (typeof app.callbackChangeView === "function") { app.callbackChangeView(); }
    });
};

app.fnChangeLocation = function() {
    if (window.history.pushState) {
        window.history.pushState(null , null, app.href);
    } else {
        window.location.href = app.href;
    }
    $("html, body").scrollTop(0);
    $("#content_wrapper").load(app.href + " #content_wrapper > *", app.fnChangeView);
};

app.fnNavCollapse = function() {
    if ($("#nav_collapse").is(":visible")) {
        side_toggle = true;
        $("#nav_toggle").trigger("click");
        $("#nav_toggle").hide();
        $("#nav_external").unbind();
        $("#nav_admin").unbind();
        $("#nav_time").unbind();
        $("#nav_email").unbind();
        $("#nav_upload").unbind();
        $("#nav_profile").unbind();

        $("#nav_logo").css("width", "auto");
    } else {
        $("#nav_toggle").show();
        $("#nav_external").hover(
          function(){ $("#nav_external_text").fadeIn(250).siblings().css("color", "#ff912e"); },
          function(){ $("#nav_external_text").fadeOut(250).siblings().css("color", "#fff"); }
        );
        $("#nav_admin").hover(
          function(){ $("#nav_admin_text").fadeIn(250).siblings().css("color", "#ff5c2b"); },
          function(){ $("#nav_admin_text").fadeOut(250).siblings().css("color", "#fff"); }
        );

        $(".dropdown-toggle").dropdown();
        $(".dropdown").hover(
          function(){ $(this).addClass("open"); },
          function(){ $(this).removeClass("open"); }
        );
        $("#nav_logo").css("width", parseInt($("#nav_logo").css("width")) + 250 - parseInt($("#nav_external").position().left));
    }
    setTimeout(function() {
        $("#page-content-wrapper").css("width", $(window).width() - $("#sidebar-wrapper").width());
        $("#wrapper").css("width", $("#sidebar-wrapper").width() + $("#page-content-wrapper").width() - 15);
    }, 500);
};

app.fnOnLoad = function() {
    $("ul.breadcrumb").css({"border-radius":"0px", "height":"50px"}).addClass("lead");
    $("ul.breadcrumb > li:first").prepend('<span style="color: #000;" class="glyphicon glyphicon-home"></span>&nbsp;&nbsp;');
    app.fnChangeView();

    $("#nav_toggle").on("click", function() {
        if (side_toggle) {
            $(".nav-ul").hide();
            $(".nav-ul-lg").fadeIn(500);
            $("#wrapper").css("padding-left", "50px");
            $("#sidebar-wrapper").css({"margin-left":"-65px", "left":"65px", "width":"65px"});
        } else {
            $("#wrapper").css("padding-left", "235px");
            $("#sidebar-wrapper").css({"margin-left":"-250px", "left":"250px", "width":"250px"});
            setTimeout(function() {
                $(".nav-ul-lg").hide();
                $(".nav-ul").not(".nav-ul-lg").fadeIn(100);
            }, 400);
        }
        side_toggle = !side_toggle;
        setTimeout(function() {
            $("#page-content-wrapper").css("width", $(window).width() - $("#sidebar-wrapper").width());
        }, 500);
    });
    $("#wrapper").css("width", $("#wrapper").width() + 15);
    app.fnNavCollapse();

    $.ajax({
        url : "/get_staff/",
        dataType: "json",
        success: function (data) {
            $("#form_email_to").val(data.admin);
            $("#form_email_to_disp").val(data.admin);
        }
    });

    $.ajax({
        url : "/group/dash/user/",
        dataType: "json",
        success: function (data) {
            app.user = data;
            if (data.photo) {
                $("#nav_user_photo").html(data.photo);
            } else {
                $("#nav_user_photo").html('<img src="/site_media/images/icon_default_avatar.png" width="119" style="padding-bottom:50px;">');
            }
            $("#nav_user_name").html(data.name);
            $("#nav_user_id").html(data.id);
            $("#nav_user_aff").html(data.title);
            $("#nav_user_stat").html(data.status);
            $("#nav_user_cap").attr("href", data.cap);
            $("#id_email_from").val(data.email);
            $("#nav_user_email").html(data.email);
            $("#nav_user_email").attr("href", "mailto:" + data.email);

            if (data.type == 'admin') {
                $("#nav_user_type").addClass("label-violet").html('<span class="glyphicon glyphicon-king" aria-hidden="true"></span>&nbsp;&nbsp;Administrator');
            } else if (data.type == 'group') {
                $("#nav_user_type").addClass("label-green").html('<span class="glyphicon glyphicon-queen" aria-hidden="true"></span>&nbsp;&nbsp;Current Member');
            } else if (data.type == 'alumni') {
                $("#nav_user_type").addClass("label-info").html('<span class="glyphicon glyphicon-pawn" aria-hidden="true"></span>&nbsp;&nbsp;Alumni Member');
            } else if (data.type == 'roton') {
                $("#nav_user_type").addClass("label-orange").html('<span class="glyphicon glyphicon-bishop" aria-hidden="true"></span>&nbsp;&nbsp;Rotation Student');
            } else if (data.type == 'other') {
                $("#nav_user_type").addClass("label-magenta").html('<span class="glyphicon glyphicon-knight" aria-hidden="true"></span>&nbsp;&nbsp;Visitor');
            } else {
                $("#nav_user_type").addClass("label-default").html('<span class="glyphicon glyphicon-glass" aria-hidden="true"></span>&nbsp;&nbsp;Unknown');
            }
            if (data.type != 'admin') {
                $("#nav_admin").css("opacity", "0.25");
            }
        }
    });

    $("#page-content-wrapper").css("opacity", 0);
    $("#nav_load").css({"opacity": 1, "top": "-50px"}).animate({"top": "0px"}, {"duration": 200, "queue": false});
    $("body > div").css("opacity", 1);
    if (side_toggle) { $("#sidebar-wrapper").animate({"left": "0px"}, {"duration": 200, "queue": false}); }
    $("#page-content-wrapper").delay(500).fadeTo(150, 1);
};


$(document).ready(function() {
    var today = new Date();
    $("#cp_year").text(today.getFullYear());

    $(".dropdown-toggle").dropdown();
    $(".dropdown").hover(
        function() { $(this).addClass("open"); },
        function() { $(this).removeClass("open"); }
    );
    $("[data-toggle='popover']").popover({trigger: "hover"});
    $("[data-toggle='tooltip']").tooltip();

    $("#top").on("click", function() {
        event.preventDefault();
        $('#top > div').animate({'right':'-5%', 'opacity':'0'}, 125);
        $("html, body").stop().animate({'scrollTop': 0}, 250);
    });

    $("#sidebar-wrapper a, #nav_upload > a, #nav_internal > a, #nav_upload_archive, #nav_logo").on("click", function(event) {
        event.preventDefault();
        app.href = $(this).attr("href");
        $("#content").fadeTo(100, 0, app.fnChangeLocation);
    });

    app.fnOnLoad();
});


$(window).on("scroll", throttle(function() {
  if ($(this).scrollTop() > $(window).height() / 2) {
    $('#top > div').animate({'right': '0%', 'opacity': 0.85}, 125);
  } else {
    $('#top > div').animate({'right': '-5%', 'opacity': 0}, 125);
  }
}, 200, 500));

$(window).on("resize", throttle(app.fnNavCollapse, 200, 1000));

window.onpopstate = function() { location.reload(); };

