var $ = django.jQuery;
var weekdayNames = new Array('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');

$(document).ready(function() {
  $("ul.breadcrumb > li.active").text("System Dashboard");

  // $("#content").addClass("row").removeClass("row-fluid").removeClass("colM");
  $("#content > h2.content-title").remove();
  $("span.divider").remove();
  $("lspan").remove();

  $.ajax({
        url : "/admin/get_ver/",
        dataType: "json",
        success : function (data) {
            $("#id_linux").html(data.linux);
            $("#id_python").html(data.python);
            $("#id_django").html(data.django);
            $("#id_django_crontab").html(data.django_crontab);
            $("#id_django_environ").html(data.django_environ);
            $("#id_mysql").html(data.mysql);
            $("#id_apache").html(data.apache);
            $("#id_wsgi").html(data.mod_wsgi);
            $("#id_webauth").html(data.mod_webauth);
            $("#id_ssl").html(data.openssl);
            $("#id_wallet").html(data.wallet);

            $("#id_jquery").html(data.jquery);
            $("#id_bootstrap").html(data.bootstrap);
            $("#id_django_suit").html(data.django_suit);
            $("#id_django_adminplus").html(data.django_adminplus);
            $("#id_django_filemanager").html(data.django_filemanager);
            $("#id_swfobj").html(data.swfobj);
            $("#id_fullcal").html(data.fullcal);
            $("#id_moment").html(data.moment);
            $("#id_ical").html(data.icalendar);
            $("#id_gvizapi").html(data.gviz_api);

            $("#id_ssh").html(data.ssh);
            $("#id_git").html(data.git);
            $("#id_nano").html(data.nano);
            $("#id_gdrive").html(data.gdrive);
            $("#id_pandoc").html(data.pandoc);
            $("#id_boto").html(data.boto);
            $("#id_pygit").html(data.pygithub);
            $("#id_slacker").html(data.slacker);
            $("#id_dropbox").html(data.dropbox);

            $("#id_request").html(data.requests);
            $("#id_simplejson").html(data.simplejson);
            $("#id_virtualenv").html(data.virtualenv);
            $("#id_pip").html(data.pip);

            $("#id_curl").html(data.curl);
            $("#id_yui").html(data.yuicompressor);
        }
    });
    $.ajax({
        url : "/admin/get_sys/",
        dataType: "json",
        success : function (data) {
            var drive_used = parseFloat(data.drive[0]), drive_free = parseFloat(data.drive[1]), drive_total = parseFloat(data.drive[2]);
            $("#id_drive_space > div > div.progress-bar-success").css("width", (drive_free / drive_total * 100).toString() + '%' ).html(drive_free + ' G');
            $("#id_drive_space > div > div.progress-bar-danger").css("width", (100 - drive_free / drive_total * 100).toString() + '%' ).html(drive_used + ' G');
            $("#id_disk_space > div > div.progress-bar-success").css("width", (parseFloat(data.disk[0]) / (parseFloat(data.disk[0]) + parseFloat(data.disk[1])) * 100).toString() + '%' ).html(data.disk[0]);
            $("#id_disk_space > div > div.progress-bar-danger").css("width", (parseFloat(data.disk[1]) / (parseFloat(data.disk[0]) + parseFloat(data.disk[1])) * 100).toString() + '%' ).html(data.disk[1]);
            $("#id_memory > div > div.progress-bar-success").css("width", (parseFloat(data.memory[0]) / (parseFloat(data.memory[0]) + parseFloat(data.memory[1])) * 100).toString() + '%' ).html(data.memory[0]);
            $("#id_memory > div > div.progress-bar-danger").css("width", (parseFloat(data.memory[1]) / (parseFloat(data.memory[0]) + parseFloat(data.memory[1])) * 100).toString() + '%' ).html(data.memory[1]);
            $("#id_cpu").html('<span style="color:#f00;">' + data.cpu[0] + '</span> | <span style="color:#080;">' + data.cpu[1] + '</span> | <span style="color:#00f;">' + data.cpu[2] + '</span>');

            $("#id_base_dir").html('<code>' + data.path.root + '</code>');
            $("#id_media_root").html('<code>' + data.path.media + '</code>');
            $("#id_static_root").html('<code>' + data.path.data + '</code>');

            $("#id_ssl_exp").html('<span class="label label-inverse">' + data.ssl_cert + '</span> (UTC)');
        }
    });
    $.ajax({
        url : "/admin/get_backup/",
        dataType: "json",
        success : function (data) {
            $("#id_backup").html('<span style="color:#00f;">' + data.backup.all + '</span>');
        }
    });

    $.ajax({
        url : "/admin/backup_form/",
        dataType: "json",
        success : function (data) {
            $("#id_week_backup").html($("#id_week_backup").html() + '<br/>On <span class="label label-primary">' + data.time_backup + '</span> every <span class="label label-inverse">' + weekdayNames[data.day_backup] + '</span> (UTC)');
            $("#id_week_upload").html($("#id_week_upload").html() + '<br/>On <span class="label label-primary">' + data.time_upload + '</span> every <span class="label label-inverse">' + weekdayNames[data.day_upload] + '</span> (UTC)');

            if (data.time_backup) {
                $("#id_week_backup_stat").html('<p class="lead"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></p>');
            } else {
                $("#id_week_backup_stat").html('<p class="lead"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></p>');
            }
            if (data.time_upload) {
                $("#id_week_upload_stat").html('<p class="lead"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></p>');
            } else {
                $("#id_week_upload_stat").html('<p class="lead"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></p>');
            }
        }
    });

    $.ajax({
        url : "/admin/dash_dash/",
        dataType: "json",
        success : function (data) {
            $("#id_dash_aws").html(data.t_aws + '<span class="label label-orange pull-right"><span class="glyphicon glyphicon-fire"></span></span>');
            $("#id_dash_ga").html(data.t_ga + '<span class="label label-orange pull-right"><span class="glyphicon glyphicon-fire"></span></span>');
            $("#id_dash_git").html(data.t_git + '<span class="label label-violet pull-right"><span class="glyphicon glyphicon-leaf"></span></span>');
            $("#id_dash_slack").html(data.t_slack + '<span class="label label-green pull-right"><span class="glyphicon glyphicon-tint"></span></span>');
            $("#id_dash_dropbox").html(data.t_dropbox + '<span class="label label-violet pull-right"><span class="glyphicon glyphicon-leaf"></span></span>');
            $("#id_dash_cal").html(data.t_cal + '<span class="label label-violet pull-right"><span class="glyphicon glyphicon-leaf"></span></span>');
            $("#id_dash_sch").html(data.t_sch + '<span class="label label-violet pull-right"><span class="glyphicon glyphicon-leaf"></span></span>');
            $("#id_dash_duty").html(data.t_duty + '<span class="label label-violet pull-right"><span class="glyphicon glyphicon-leaf"></span></span>');
        }
    });



});

