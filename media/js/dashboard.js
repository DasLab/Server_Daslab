        // f = open('src/sys_ver.txt', 'r')
        // (ver_linux, ver_python, ver_cherrypy, ver_matlab, ver_rdatkit, ver_jquery, ver_bootstrap, ver_ssh, ver_screen, ver_tty, ver_apache, ver_git, ver_gcc, ver_clang, ver_cmake, ver_numpy, ver_scipy, ver_matplotlib, ver_celery, ver_simplejson, ver_setuptools, ver_pip, ver_octave, disk_sp, mem_sp, cache_n, cache_sz, path_primerize, path_nathermo, path_rdatkit, path_python, path_matlab) = tuple(f.readlines()[0].split('\t'))
        // disk_sp = '<span style="color:#080;">' + disk_sp[:disk_sp.find('/')] + '</span>/<span style="color:#f00;">' + disk_sp[disk_sp.find('/')+1:] + '</span>'
        // mem_sp = '<span style="color:#080;">' + mem_sp[:mem_sp.find('/')] + '</span>/<span style="color:#f00;">' + mem_sp[mem_sp.find('/')+1:] + '</span>'
        // cache_sz = '<span style="color:#00f;">' + cache_sz + '</span>'
        // f.close()


$(document).ready(function() {
  $("ul.breadcrumb>li.active").text("System Dashboard");

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
        	$("#id_jquery_group").html(txt[5]);
        	$("#id_jquery_admin").html(txt[6]);
        	$("#id_bootstrap_group").html(txt[7]);
        	$("#id_bootstrap_admin").html(txt[8]);
        	$("#id_mysql").html(txt[9]);
        	$("#id_apache").html(txt[10]);
        	$("#id_webauth").html(txt[11]);
        	$("#id_ssh").html(txt[12]);
        	$("#id_git").html(txt[13]);
        	$("#id_pip").html(txt[14]);
        	$("#id_virtualenv").html(txt[15]);

        	var disk_sp = txt[16].split(/\//);
        	$("#id_disk_space").html('<span style="color:#080;">' + disk_sp[0] + '</span> / <span style="color:#f00;">' + disk_sp[1] + '</span>');
        	var mem_sp = txt[17].split(/\//);
        	$("#id_memory").html('<span style="color:#080;">' + mem_sp[0] + '</span> / <span style="color:#f00;">' + mem_sp[1] + '</span>');
        	$("#id_db_backup").html('<span style="color:#00f;">' + txt[18] + '</span>');
        	var cpu = txt[19].split(/\//);
        	$("#id_cpu").html('<span style="color:#f00;">' + cpu[0] + '</span> / <span style="color:#080;">' + cpu[1] + '</span> / <span style="color:#00f;">' + cpu[2] + '</span>');

        	$("#id_news_n").html('<i>' + txt[20] + '</i>');
        	$("#id_news_s").html('<span style="color:#00f;">' + txt[21] + '</span>');
        	$("#id_member_n").html('<i>' + txt[22] + '</i>');
        	$("#id_member_s").html('<span style="color:#00f;">' + txt[23] + '</span>');
        	$("#id_pub_n").html('<i>' + txt[24] + '</i>');
        	$("#id_pub_s").html('<span style="color:#00f;">' + txt[25] + '</span>');
        	$("#id_rot_n").html('<i>' + txt[26] + '</i>');
        	$("#id_rot_s").html('<span style="color:#00f;">' + txt[27] + '</span>');
        	$("#id_spe_n").html('<i>' + txt[28] + '</i>');
        	$("#id_spe_s").html('<span style="color:#00f;">' + txt[29] + '</span>');
    	}
    });


});

