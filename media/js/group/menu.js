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
        url : "/admin/user_dash",
        dataType: "json",
        success: function (data) {
            $("#nav_user_photo").html(data.photo);
            $("#nav_user_name").html(data.name);
            $("#nav_user_id").html(data.id);
            $("#nav_user_aff").html(data.title);
            $("#nav_user_stat").html(data.status);
            $("#nav_user_cap").attr("href", data.cap);
            $("#form_email_from").val(data.email);

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

    $("#form_email_clear").on("click", function() {
        $("#form_email_from").val('');
        $("#form_email_subject").val('');
        $("#form_email_content").val('');
    });

    $("#form_email").submit(function(event) {
        $("#form_email_msg").parent().addClass("alert-warning").removeClass("alert-danger").removeClass("alert-success");
        $("#form_email_notice > div > div > p > span").removeClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").addClass("glyphicon-hourglass");
        $("#form_email_notice > div > div > p > b").html('SENDING');
        $("#form_email_msg").html('');
        $("#form_email_notice").fadeIn();
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(data)
            {
                if (data.messages == 'invalid') {
                    $("#form_email_msg").parent().addClass("alert-danger").removeClass("alert-warning").removeClass("alert-success");
                    $("#form_email_notice > div > div > p > span").addClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").removeClass("glyphicon-hourglass");
                    $("#form_email_notice > div > div > p > b").html('ERROR');
                    $("#form_email_msg").html('Incomplete email fields. Please try again.');
                } else if (data.messages == 'success') {
                    $("#form_email_msg").parent().addClass("alert-success").removeClass("alert-warning").removeClass("alert-danger");
                    $("#form_email_notice > div > div > p > span").addClass("glyphicon-ok-sign").removeClass("glyphicon-remove-sign").removeClass("glyphicon-hourglass");
                    $("#form_email_notice > div > div > p > b").html('SUCCESS');
                    $("#form_email_msg").html('Email sent. The Admin WILL read it!');
                }
                setTimeout(function() { $("#form_email_notice").fadeOut(); }, 2500);
            },
            error: function() {
                $("#form_email_msg").parent().addClass("alert-danger").removeClass("alert-warning").removeClass("alert-success");
                $("#form_email_notice > div > div > p > span").addClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").removeClass("glyphicon-hourglass");
                $("#form_email_notice > div > div > p > b").html('ERROR');
                $("#form_email_msg").html('Internal Server Error.');
             }
        });

        event.preventDefault();
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

