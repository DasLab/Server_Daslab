var side_toggle = true, apache_interval;
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
        "sys": ["apache", "aws", "ga", "git", "dir", "backup", "bot"],
        "global": ["news", "member", "publication", "export"],
        "internal": ["auth", "flashslide", "journalclub", "eternayoutube", "rotationstudent", "presentation", "defenseposter", "slackmessage"],
        "doc": ["man", "ref", "key"]
    };
    var page = window.location.pathname.replace('/admin', '').replace(/^\//, '').split('/');
    app.page = (page[0] == "src")? page[1] : page[0];
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
    if (app.key == "sys") {
        if (app.page == "dir" || app.page == "backup" || app.page == "bot") {
            $("ul.breadcrumb").css("border-bottom", "5px solid #ff69bc");
        } else {
            $("ul.breadcrumb").css("border-bottom", "5px solid #ff5c2b");
        }
        $('<li><span style="color: #000;" class="glyphicon glyphicon-cog"></span>&nbsp;&nbsp;<a href="">System</a></li>').insertAfter($("ul.breadcrumb > li:first"));

        if (app.page == "apache") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-grain"></span>&nbsp;&nbsp;Apache Status</li>');
        } else if (app.page == "aws") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_aws"></i></div>&nbsp;&nbsp;Amazon Web Services</li>');
        } else if (app.page == "ga") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_ga"></i></div>&nbsp;&nbsp;Google Analytics</li>');
        } else if (app.page == "git") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_git"></i></div>&nbsp;&nbsp;GitHub Repository</li>');
        } else if (app.page == "dir") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-folder-open"></span>&nbsp;&nbsp;Directory Browser</li>');
        } else if (app.page == "backup") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-floppy-open"></span>&nbsp;&nbsp;Backup Schedule</li>');
        } else if (app.page == "bot") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_bot"></i></div>&nbsp;&nbsp;DasLab Bot Settings</li>');
        }

    } else if (app.key == "global") {
        if (app.page == "export") {
            $("ul.breadcrumb").css("border-bottom", "5px solid #008080");
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-floppy-save"></span>&nbsp;&nbsp;Publication Export</li>');
        } else {
            $("ul.breadcrumb").css("border-bottom", "5px solid #50cc32");
            $("ul.breadcrumb > li:first").next().remove();

            if (app.page == "news") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-picture"></span>&nbsp;&nbsp;News Items</li>');
            } else if (app.page == "member") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Member Management</li>');
            } else if (app.page == "publication") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-education"></span>&nbsp;&nbsp;Publication Entries</li>');
            }
        }

        $('<li><span style="color: #000;" class="glyphicon glyphicon-globe"></span>&nbsp;&nbsp;<a href="">Global Site</a></li>').insertAfter($("ul.breadcrumb > li:first"));

    } else if (app.key == "internal") {
        if (app.page == "auth") {
            $("ul.breadcrumb").css("border-bottom", "5px solid #ff912e");
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-lock"></span>&nbsp;&nbsp;User Autherization</li>');
        } else {
            $("ul.breadcrumb").css("border-bottom", "5px solid #eeb211");

            if (app.page == "flashslide") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-blackboard"></span>&nbsp;&nbsp;Flash Slides</li>');
            } else if (app.page == "journalclub") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-book"></span>&nbsp;&nbsp;Journal Clubs</li>');
            } else if (app.page == "eternayoutube") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-facetime-video"></span>&nbsp;&nbsp;EteRNA Videos</li>');
            } else if (app.page == "rotationstudent") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-retweet"></span>&nbsp;&nbsp;Rotation Students</li>');
            } else if (app.page == "presentation") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-cd"></span>&nbsp;&nbsp;Archived Presentations</li>');
            } else if (app.page == "defenseposter") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-scissors"></span>&nbsp;&nbsp;Defense Posters</li>');
            } else if (app.page == "slackmessage") {
                $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_slack"></i></div>&nbsp;&nbsp;Slack Messages</li>');
            }
        }
        $('<li><span style="color: #000;" class="glyphicon glyphicon-inbox"></span>&nbsp;&nbsp;<a href="">Internal Site</a></li>').insertAfter($("ul.breadcrumb > li:first"));

    } else if (app.key == "doc") {
        $("#nav_doc_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #c28fdd");

        if (app.page == "man") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-scale"></span>&nbsp;&nbsp;Manual</li>');
        } else if (app.page == "ref") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-briefcase"></span>&nbsp;&nbsp;Reference</li>');
        } else if (app.page == "key") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-usd"></span>&nbsp;&nbsp;Secrets</li>');
        }

    } else {
        $("ul.breadcrumb").css("border-bottom", "5px solid #3ed4e7");
    }
};

app.fnChangeView = function() {
    app.fnParseLocation();
    $("#sidebar-wrapper ul li.active").removeClass("active");
    $("#nav_" + app.page).addClass("active");
    $("#nav_" + app.key).addClass("active");
    $("#nav_" + app.key + "_lg").addClass("active");

    app.fnChangeBreadcrumb();
    $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'page' + app.DEBUG_STR + '.js', function(data, code, xhr) {
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
        $("#nav_group").unbind();
        $("#nav_time").unbind();
        $("#nav_email").unbind();
        $("#nav_upload").unbind();
        // $("#nav_profile").unbind();

        $("#nav_logo").css("width", "auto");
    } else {
        $("#nav_toggle").show();
        // $("#nav_time").hover(
        //   function(){ $("#nav_meetings").fadeIn(); },
        //   function(){ $("#nav_meetings").fadeOut(); }
        // );
        $("#nav_external").hover(
          function(){ $("#nav_external_text").fadeIn(250).siblings().css("color", "#ff912e"); },
          function(){ $("#nav_external_text").fadeOut(250).siblings().css("color", "#fff"); }
        );
        $("#nav_group").hover(
          function(){ $("#nav_group_text").fadeIn(250).siblings().css("color", "#eeb211"); },
          function(){ $("#nav_group_text").fadeOut(250).siblings().css("color", "#fff"); }
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

    $('i[class^="icon"]').each(function() {
        $(this).replaceWith('<span class="glyphicon glyph' + $(this).attr("class") + '"></span>&nbsp;&nbsp;');
    });

    $("#sidebar-wrapper a, #nav_admin > a, #nav_logo").on("click", function(event) {
        event.preventDefault();
        app.href = $(this).attr("href");
        $("#content").fadeTo(100, 0, app.fnChangeLocation);
    });

    app.fnOnLoad();
});


$(window).on("resize", throttle(app.fnNavCollapse, 200, 1000));
window.onpopstate = function() { location.reload(); };

