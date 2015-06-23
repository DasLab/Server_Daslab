var $ = django.jQuery;

$(document).ready(function() {
  $("ul.breadcrumb>li.active").text("System Dashboard");

  $("#content").addClass("row").removeClass("row-fluid").removeClass("colM");
  $("#content>h2.content-title").remove();
  $("span.divider").remove();
  $("lspan").remove();

  $.ajax({
        url : "/site_data/sys_ver.txt",
        dataType: "text",
        success : function (data) {
        	var txt = data.split(/\t/);

        	$("#id_linux").html(txt[0]);
        	$("#id_python").html(txt[1]);
        	$("#id_django").html(txt[2]);
        	$("#id_django_suit").html(txt[3]);
        	$("#id_django_adminplus").html(txt[4]);
        	$("#id_jquery").html(txt[5]);
        	$("#id_bootstrap").html(txt[6]);
        	$("#id_mysql").html(txt[7]);
        	$("#id_apache").html(txt[8]);
        	$("#id_webauth").html(txt[9]);
        	$("#id_ssh").html(txt[10]);
        	$("#id_git").html(txt[11]);
        	$("#id_pip").html(txt[12]);
        	$("#id_virtualenv").html(txt[13]);

        	var disk_sp = txt[14].split(/\//);
        	$("#id_disk_space").html('<span style="color:#080;">' + disk_sp[0] + '</span> / <span style="color:#f00;">' + disk_sp[1] + '</span>');
        	var mem_sp = txt[15].split(/\//);
        	$("#id_memory").html('<span style="color:#080;">' + mem_sp[0] + '</span> / <span style="color:#f00;">' + mem_sp[1] + '</span>');
        	$("#id_db_backup").html('<span style="color:#00f;">' + txt[16] + '</span>');
        	var cpu = txt[17].split(/\//);
        	$("#id_cpu").html('<span style="color:#f00;">' + cpu[0] + '</span> / <span style="color:#080;">' + cpu[1] + '</span> / <span style="color:#00f;">' + cpu[2] + '</span>');

        	$("#id_news_n").html('<i>' + txt[18] + '</i>');
        	$("#id_news_s").html('<span style="color:#00f;">' + txt[19] + '</span>');
        	$("#id_member_n").html('<i>' + txt[20] + '</i>');
        	$("#id_member_s").html('<span style="color:#00f;">' + txt[21] + '</span>');
        	$("#id_pub_n").html('<i>' + txt[22] + '</i>');
        	$("#id_pub_s").html('<span style="color:#00f;">' + txt[23] + '</span>');
        	$("#id_rot_n").html('<i>' + txt[24] + '</i>');
        	$("#id_rot_s").html('<span style="color:#00f;">' + txt[25] + '</span>');
        	$("#id_spe_n").html('<i>' + txt[26] + '</i>');
        	$("#id_spe_s").html('<span style="color:#00f;">' + txt[27] + '</span>');

            $("#id_base_dir").html('<code>' + txt[28] + '</code>');
            $("#id_media_root").html('<code>' + txt[29] + '</code>');
            $("#id_static_root").html('<code>' + txt[30] + '</code>');
    	}
    });


});

