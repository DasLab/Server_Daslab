setInterval(function () {
    var utc = new Date().toISOString().replace(/\..+/, '.000Z');
    $("#utc").html(utc);
}, 1000);


$(document).ready(function () {
    $(".nav-ul-lg").css("display", "none");
    var side_toggle = true;

    if ($(location).attr("href").indexOf("group/schedule") != -1) {
        $("#nav_schedule").addClass("active");
        $("#nav_meeting").addClass("active");
        $("#nav_meeting_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff5c2b");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-bell"></span>&nbsp;&nbsp;<a href="">Group Meeting</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/flash_slide") != -1) {
        $("#nav_flash").addClass("active");
        $("#nav_meeting").addClass("active");
        $("#nav_meeting_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff5c2b");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-bell"></span>&nbsp;&nbsp;<a href="">Group Meeting</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/youtube") != -1) {
        $("#nav_eterna").addClass("active");
        $("#nav_meeting").addClass("active");
        $("#nav_meeting_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff5c2b");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-bell"></span>&nbsp;&nbsp;<a href="">Group Meeting</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/rotation") != -1) {
        $("#nav_rotation").addClass("active");
        $("#nav_meeting").addClass("active");
        $("#nav_meeting_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff5c2b");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-bell"></span>&nbsp;&nbsp;<a href="">Group Meeting</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/gdocs") != -1) {
        $("#nav_gdocs").addClass("active");
        $("#nav_res").addClass("active");
        $("#nav_res_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #eeb211");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-briefcase"></span>&nbsp;&nbsp;<a href="">Resources</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/archive") != -1) {
        $("#nav_archive").addClass("active");
        $("#nav_res").addClass("active");
        $("#nav_res_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #eeb211");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-briefcase"></span>&nbsp;&nbsp;<a href="">Resources</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/aws") != -1) {
        $("#nav_aws").addClass("active");
        $("#nav_server").addClass("active");
        $("#nav_server_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #50cc32");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;<a href="">Servers</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/ga") != -1) {
        $("#nav_ga").addClass("active");
        $("#nav_server").addClass("active");
        $("#nav_server_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #50cc32");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;<a href="">Servers</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/git") != -1) {
        $("#nav_git").addClass("active");
        $("#nav_service").addClass("active");
        $("#nav_service_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff912e");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;<a href="">Services</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/slack") != -1) {
        $("#nav_slack").addClass("active");
        $("#nav_service").addClass("active");
        $("#nav_service_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff912e");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;<a href="">Services</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/dropbox") != -1) {
        $("#nav_dropbox").addClass("active");
        $("#nav_service").addClass("active");
        $("#nav_service_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #ff912e");
        $('<li><span style="color: #000;" class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;<a href="">Services</a></li>').insertAfter($("ul.breadcrumb > li:first"));
    } else if ($(location).attr("href").indexOf("group/calendar") != -1) {
        $("#nav_cal").addClass("active");
        $("#nav_cal_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #c28fdd");
    } else if ($(location).attr("href").indexOf("group/misc") != -1) {
        $("#nav_misc").addClass("active");
        $("#nav_misc_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #5496d7");
    } else {
        $("#nav_home").addClass("active");
        $("#nav_home_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #3ed4e7");
    }

    $("#nav_toggle").on("click", function() {
        if (side_toggle) {
            $(".nav-ul").hide();
            $(".nav-ul-lg").show();
            $("#wrapper").css("padding-left", "50px");
            $("#sidebar-wrapper").css({"margin-left":"-65px", "left":"65px", "width":"65px"});
        } else {
            $(".nav-ul-lg").hide();
            $(".nav-ul").not(".nav-ul-lg").show();
            $("#wrapper").css("padding-left", "235px");
            $("#sidebar-wrapper").css({"margin-left":"-250px", "left":"250px", "width":"250px"});
        }
        side_toggle = !side_toggle;
    });
    $("#wrapper").css("width", (parseInt($("#wrapper").css("width")) + 15).toString() + "px");

    $("ul.breadcrumb").css({"border-radius":"0px", "height":"50px"}).addClass("lead");
    $("ul.breadcrumb > li:first").prepend('<span style="color: #000;" class="glyphicon glyphicon-home"></span>&nbsp;&nbsp;');

    $("#nav_time").hover(
      function(){ $("#nav_meetings").fadeIn(); },
      function(){ $("#nav_meetings").fadeOut(); }
    );
    $("#nav_external").hover(
      function(){ $("#nav_external_text").fadeIn().siblings().css("color", "#ff912e"); },
      function(){ $("#nav_external_text").fadeOut().siblings().css("color", "#fff"); }
    );
    $("#nav_admin").hover(
      function(){ $("#nav_admin_text").fadeIn().siblings().css("color", "#ff5c2b"); },
      function(){ $("#nav_admin_text").fadeOut().siblings().css("color", "#fff"); }
    );
    $(".dropdown-toggle").dropdown();
    $(".dropdown").hover(
      function(){ $(this).addClass("open"); },
      function(){ $(this).removeClass("open"); }
    );
    $("#nav_logo").css("width", parseInt($("#nav_logo").css("width")) + 250 - parseInt($("#nav_external").position().left));

    // $('.left-nav > ul > li > ul > li > a[href="/admin/aws/"]').attr("disabled", "disabled").css("text-decoration", "line-through").attr("href", "");
});
