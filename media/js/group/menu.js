var side_toggle = true;

function navbar_collapse() {
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
        // $("#nav_time").hover(
        //   function(){ $("#nav_meetings").fadeIn(); },
        //   function(){ $("#nav_meetings").fadeOut(); }
        // );
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

}


$(document).ready(function () {
    $(".nav-ul-lg").css("display", "none");

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
    } else if ($(location).attr("href").indexOf("group/contact") != -1) {
        $("#nav_contact").addClass("active");
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

    $(".dropdown-toggle").dropdown();
    $(".dropdown").hover(
      function(){ $(this).addClass("open"); },
      function(){ $(this).removeClass("open"); }
    );
    navbar_collapse();

    $.ajax({
        url : "/get_admin",
        dataType: "json",
        success: function (data) {
            $("#form_email_to").val(data.email);
            $("#form_email_to_disp").val(data.email);
        }
    });

    $.ajax({
        url : "/group/user_dash",
        dataType: "json",
        success: function (data) {
            $("#nav_user_photo").html(data.photo);
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

            if ($(location).attr("href").indexOf("group/contact") != -1) {
                $("#card_user_photo").html(data.photo);
                $("#card_user_photo > img").css("max-width", "100%");
                $("#card_user_name").html(data.name);
                $("#card_user_id").html(data.id);
                $("#card_user_aff").html(data.title);
                $("#card_user_stat").html(data.status);
                $("#card_user_cap").attr("href", data.cap);
                $("#card_user_email").html(data.email);
                $("#card_user_email").attr("href", "mailto:" + data.email);
                $("#form_change_email").val(data.email);
                $("#card_user_phone").html(data.phone);
                $("#form_change_phone").val(data.phone.replace(/\D+/g, ''));
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#form_change_email").attr("disabled", "disabled");
            $("#form_change_phone").attr("disabled", "disabled");
            $("#form_change_submit").attr("disabled", "disabled");

            if (errorThrown == 'BAD REQUEST') {
                $("#nav_user_photo").html('<img src="/site_media/images/group/fg_load.gif" width="119" style="padding-bottom:50px;">');
                $("#nav_user_name").html('DasLab Admin');
                $("#nav_user_id").html('daslab');
                $("#nav_user_aff").html('Shared <span class="label label-success">Admin</span> Account');
                $("#nav_user_stat").html('N/A');
                if ($(location).attr("href").indexOf("group/contact") != -1) {
                    $("#card_user_photo").html('<img src="/site_media/images/group/fg_load.gif" width="119">');
                    $("#card_user_photo > img").css("max-width", "100%");
                    $("#card_user_name").html('DasLab Admin');
                    $("#card_user_id").html('daslab');
                    $("#card_user_aff").html('Shared <span class="label label-success">Admin</span> Account');
                    $("#card_user_stat").html('N/A');
                    $("#card_user_email").html('daslabsu@gmail.com');
                    $("#card_user_email").attr("href", "mailto:daslabsu@gmail.com");
                    $("#card_user_phone").html('(650) 723-7310');
                }          
            } else {
                $("#nav_user_photo").html('<img src="/site_media/images/group/fg_loadicon_default_avatar.png" width="119" style="padding-bottom:50px;">');
                $("#nav_user_name").html('Unknown');
                $("#nav_user_id").html('N/A');
                $("#nav_user_aff").html('Unknown');
                $("#nav_user_stat").html('Rotation Student / Temporary');
                if ($(location).attr("href").indexOf("group/contact") != -1) {
                    $("#card_user_photo").html('<img src="/site_media/images/icon_default_avatar.png" width="119">');
                    $("#card_user_photo > img").css("max-width", "100%");
                    $("#card_user_name").html('Unknown');
                    $("#card_user_id").html('N/A');
                    $("#card_user_aff").html('Unknown');
                    $("#card_user_stat").html('Rotation Student / Temporary');
                    $("#card_user_email").html('Unknown');
                    $("#card_user_phone").html('Unknown');
                }                
            }

        }
    });

    // $('.left-nav > ul > li > ul > li > a[href="/admin/aws/"]').attr("disabled", "disabled").css("text-decoration", "line-through").attr("href", "");
});


$(window).on("resize", function() {
    clearTimeout($.data(this, 'resizeTimer'));
    $.data(this, 'resizeTimer', setTimeout(function() {
        navbar_collapse();
        $("#wrapper").css("width", $(window).width() - $("sidebar-wrapper").width() - 20);
    }, 200));
});

