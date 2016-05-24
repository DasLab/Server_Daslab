function replace_path(string) {
    return string.replace('/home/ubuntu/Server_DasLab/data/', '/site_data/').replace('/Website_Server/Daslab/data/', '/site_data/');
}

$(document).ready(function () {
    // $('script[src="/static/admin/js/admin/DateTimeShortcuts.js"]').remove();
    // $('script[src="/static/admin/js/jquery.js"]').remove();
    // $('script[src="/static/admin/js/jquery.init.js"]').remove();

    if ($(location).attr("href").indexOf("admin/src/news") != -1) {
        $("th.column-date").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-content").addClass("col-lg-6 col-md-6 col-sm-6 col-xs-6");
        $("th.column-link").addClass("col-lg-4 col-md-4 col-sm-4 col-xs-4");

        $("td.field-link").css({"word-break":"break-all", "text-decoration":"underline"});
        $("td.field-content").each(function() { $(this).html($(this).text()); });

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Date');
        $("th.column-content > div.text > a").html('<span class="glyphicon glyphicon-list-alt"></span>&nbsp;&nbsp;Content');
        $("th.column-link > div.text > a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;&nbsp;URL');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-picture"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/publication") != -1) {
        $("th.column-year").addClass("col-lg-1 col-md-1 col-sm-1 col-xs-1");
        $("th.column-journal").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-authors").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-title").addClass("col-lg-4 col-md-4 col-sm-4 col-xs-4");
        $("th.column-link").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");

        $("td.field-authors").css("word-break", "break-all");
        $("td.field-title").css({"word-break":"break-all", "font-weight":"bold"});
        $("td.field-link").css({"word-break":"break-all", "text-decoration":"underline"});
        $("td.field-journal").css("font-style", "italic");

        $("th.column-year > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Year');
        $("th.column-journal > div.text > a").html('<span class="glyphicon glyphicon-book"></span>&nbsp;&nbsp;Journal');
        $("th.column-authors > div.text > a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Authors');
        $("th.column-title > div.text > a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Title');
        $("th.column-link > div.text > a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;&nbsp;URL');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-education"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/member") != -1) {
        $("th.column-full_name").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-sunet_id").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-year").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-joint_lab").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-affiliation").addClass("col-lg-4 col-md-4 col-sm-4 col-xs-4");

        $("th.field-full_name").css("font-weight", "bold");
        $("td.field-sunet_id").each(function() { $(this).html("<kbd>" + $(this).html() + "</kbd>"); });

        $("th.column-full_name > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Full Name');
        $("th.column-sunet_id > div.text > a").html('<span class="glyphicon glyphicon-qrcode"></span>&nbsp;&nbsp;SUNet ID');
        $("th.column-year > div.text > a").html('<span class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;Status');
        $("th.column-joint_lab > div.text > a").html('<span class="glyphicon glyphicon-home"></span>&nbsp;&nbsp;Joint Lab');
        $("th.column-affiliation > div.text > a").html('<span class="glyphicon glyphicon-education"></span>&nbsp;&nbsp;Affiliation');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-user"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/flashslide") != -1) {
        $("th.column-date").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-link").addClass("col-lg-9 col-md-9 col-sm-9 col-xs-9");

        $("td.field-link").css("text-decoration", "underline");

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Date');
        $("th.column-link > div.text > a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;&nbsp;URL');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-blackboard"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/journalclub") != -1) {
        $("th.column-date").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-presenter").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-title").addClass("col-lg-5 col-md-5 col-sm-5 col-xs-5");
        $("th.column-link").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");

        $("td.field-link").css("text-decoration", "underline");
        $("td.field-presenter").css("font-weight", "bold");

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Date');
        $("th.column-presenter > div.text > a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Presenter');
        $("th.column-title > div.text > a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Title');
        $("th.column-link > div.text > a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;&nbsp;URL');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-book"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/rotationstudent") != -1) {
        $("th.column-date").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-full_name").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-title").addClass("col-lg-6 col-md-6 col-sm-6 col-xs-6");

        $("td.field-full_name").css("font-weight", "bold");

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Date');
        $("th.column-full_name > div.text > a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Student');
        $("th.column-title > div.text > a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Title');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-retweet"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/eternayoutube") != -1) {
        $("th.column-date").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-presenter").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-title").addClass("col-lg-5 col-md-5 col-sm-5 col-xs-5");
        $("th.column-link").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");

        $("td.field-presenter").css("font-weight", "bold");
        $("td.field-link").css("text-decoration", "underline");

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Date');
        $("th.column-presenter > div.text > a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Presenter');
        $("th.column-title > div.text > a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Title');
        $("th.column-link > div.text > a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;&nbsp;URL');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-facetime-video"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/presentation") != -1) {
        $("th.column-date").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-presenter").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-title").addClass("col-lg-6 col-md-6 col-sm-6 col-xs-6");

        $("td.field-presenter").css("font-weight", "bold");

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Date');
        $("th.column-presenter > div.text > a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Student');
        $("th.column-title > div.text > a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Title');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-cd"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/slackmessage") != -1) {
        $("th.column-date").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-receiver").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-message").addClass("col-lg-8 col-md-8 col-sm-8 col-xs-8");

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Date');
        $("th.column-receiver > div.text > a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Receiver');
        $("th.column-message > div.text > a").html('<span class="glyphicon glyphicon-compressed"></span>&nbsp;&nbsp;Message (Content + Attachment)');

        $("td.field-receiver").each(function() { $(this).html("<a>" + $(this).html() + "</a>"); });
        $("td.field-message").each(function() { $(this).html('<div class="well well-sm excerpt" style="font-family:monospace; font-size:12px; margin-bottom:0px;">' + $(this).html() + "</div>");   });

        $("div.col-md-6 > h2.legend").html('<div class="sprite i_14"><i class="i_slack"></i></div>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/auth/user") != -1) {
        $("th.column-username").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-email").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-last_login").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-is_active").addClass("col-lg-1 col-md-1 col-sm-1 col-xs-1");
        $("th.column-is_staff").addClass("col-lg-1 col-md-1 col-sm-1 col-xs-1");
        $("th.column-is_superuser").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");

        $("th.field-username").css("font-style", "italic");
        $("td.field-email").css("text-decoration", "underline");

        $("th.column-username > div.text > a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Username');
        $("th.column-email > div.text > a").html('<span class="glyphicon glyphicon-envelope"></span>&nbsp;&nbsp;Email Address');
        $("th.column-last_login > div.text > a").html('<span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;Last Login');
        $("th.column-is_active > div.text > a").html('<span class="glyphicon glyphicon-pawn"></span>&nbsp;&nbsp;Active');
        $("th.column-is_staff > div.text > a").html('<span class="glyphicon glyphicon-queen"></span>&nbsp;&nbsp;Staff');
        $("th.column-is_superuser > div.text > a").html('<span class="glyphicon glyphicon-king"></span>&nbsp;&nbsp;Admin');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-lock"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    }

});


