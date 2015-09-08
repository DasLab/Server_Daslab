function zfill(num, len) {return (Array(len).join("0") + num).slice(-len);}

$(document).ready(function() {
	$.ajax({
        url : "/admin/slack_dash?qs=users&tqx=reqId%3A52",
        dataType: "json",
        success : function (data) {
			var html = "";
			for (var i = 0; i < data.owners.length; i++) {
				html += '<tr><td><span class="pull-right"><span class="label label-danger">' + data.owners[i].id + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-registration-mark"></span></span></td><td><img src="' + data.owners[i].image + '"/>&nbsp;&nbsp;<i>' + data.owners[i].name + '</i></td></tr>';
			}
			for (var i = 0; i < data.admins.length; i++) {
				html += '<tr><td><span class="pull-right"><span class="label label-success">' + data.admins[i].id + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-copyright-mark"></span></span></td><td><img src="' + data.admins[i].image + '"/>&nbsp;&nbsp;<i>' + data.admins[i].name + '</i></td></tr>';
			}
			for (var i = 0; i < data.users.length; i++) {
				html += '<tr><td><span class="pull-right"><span class="label label-violet">' + data.users[i].id + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-ok-circle"></span></span></td><td><img src="' + data.users[i].image + '"/>&nbsp;&nbsp;<i>' + data.users[i].name + '</i></td></tr>';
			}
			html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
			for (var i = 0; i < data.gones.length; i++) {
				html += '<tr class="active"><td><span class="pull-right"><span class="label label-default">' + data.gones[i].id + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-ban-circle"></span></span></td><td><img src="' + data.gones[i].image + '"/>&nbsp;&nbsp;<i>' + data.gones[i].name + '</i></td></tr>';
			}        	
			html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
			$("#table_slack_user").html(html);
        }
    });

	$.ajax({
        url : "/admin/slack_dash?qs=channels&tqx=reqId%3A53",
        dataType: "json",
        success : function (data) {
			var html = "";
			for (var i = 0; i < data.channels.length; i++) {
				var name = "", num_msgs = data.channels[i].num_msgs.toString();
		        var time = new Date();
		        time.setTime(parseInt(data.channels[i].latest * 1000));
		        latest = time.getFullYear() + '-' + zfill(time.getMonth(), 2) + '-' + zfill(time.getDate(), 2) + ' ' + zfill(time.getHours(), 2) + ':' + zfill(time.getMinutes(), 2) + ':' + zfill(time.getSeconds(), 2);
				if (data.channels[i].name == "general" || data.channels[i].name == "random") { 
					name = '<span class="label label-info">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-play-circle">'
				} else if (data.channels[i].name == "dropbox" || data.channels[i].name == "github") { 
					name = '<span class="label label-orange">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-record">'
				} else {
					name = '<span class="label label-inverse">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-ok-circle">'
				}
				if (data.channels[i].has_more) { num_msgs = num_msgs + '+'}
				html += '<tr><td><span class="pull-right">' + name + '</span></td><td><span class="pull-right">' + data.channels[i].num_members + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + num_msgs + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + data.channels[i].num_files + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="label label-primary">' + latest + '</span></td></tr>';
			}
			html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
			for (var i = 0; i < data.archives.length; i++) {
				var num_msgs = data.archives[i].num_msgs.toString();
		        var time = new Date();
		        time.setTime(parseInt(data.archives[i].latest * 1000));
		        latest = time.getFullYear() + '-' + zfill(time.getMonth(), 2) + '-' + zfill(time.getDate(), 2) + ' ' + zfill(time.getHours(), 2) + ':' + zfill(time.getMinutes(), 2) + ':' + zfill(time.getSeconds(), 2);
				if (data.archives[i].has_more) { num_msgs = num_msgs + '+'}
				html += '<tr class="active"><td><span class="pull-right"><span class="label label-default">' + data.archives[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-ban-circle"></span></td><td><span class="pull-right">' + data.archives[i].num_members + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + num_msgs + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + data.archives[i].num_files + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="label label-primary">' + latest + '</span></td></tr>';
			}
			html += '<tr><td colspan="5" style="padding: 0px;"></td></tr>';
			$("#table_slack_channel").html(html);
        }
    });
})
