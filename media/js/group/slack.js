function zfill(num, len) {
	return (Array(len).join("0") + num).slice(-len);
}

function formatSizeUnits(bytes){
    if      (bytes >= 1000000000) {bytes = (bytes / 1000000000).toFixed(2) + ' GB';}
    else if (bytes >= 1000000)    {bytes = (bytes / 1000000).toFixed(2) + ' MB';}
    else if (bytes >= 1000)       {bytes = (bytes / 1000).toFixed(2) + ' KB';}
    else if (bytes > 1)           {bytes = bytes + ' bytes';}
    else if (bytes == 1)          {bytes = bytes + ' byte';}
    else                          {bytes = '0 byte';}
    return bytes;
}


$.ajax({
    url : "/admin/slack_dash?qs=users&tqx=reqId%3A52",
    dataType: "json",
    success: function (data) {
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

		var ratio = data.gones.length / (data.owners.length + data.admins.length + data.users.length + data.gones.length);
        $("#id_user_num > div > div.progress-bar-success").css("width", ((1 - ratio) * 100).toString() + '%' ).html(data.owners.length + data.admins.length + data.users.length);
        $("#id_user_num > div > div.progress-bar-danger").css("width", (ratio * 100).toString() + '%' ).html(data.gones.length);
    }
});

$.ajax({
    url : "/admin/slack_dash?qs=channels&tqx=reqId%3A53",
    dataType: "json",
    success: function (data) {
		var html = "";
		for (var i = 0; i < data.channels.length; i++) {
			var name = "", num_msgs = data.channels[i].num_msgs.toString();
			if (data.channels[i].name == "general" || data.channels[i].name == "random") { 
				name = '<span class="label label-info">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-play-circle">'
			} else if (data.channels[i].name == "dropbox" || data.channels[i].name == "github") { 
				name = '<span class="label label-orange">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-record">'
			} else {
				name = '<span class="label label-inverse">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-ok-circle">'
			}
			if (data.channels[i].has_more) { num_msgs = num_msgs + '+'}
			html += '<tr><td><span class="pull-right">' + name + '</span></td><td><span class="pull-right">' + data.channels[i].num_members + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + num_msgs + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + data.channels[i].num_files + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="label label-primary">' + data.channels[i].latest + '</span></td></tr>';
		}
		html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
		for (var i = 0; i < data.archives.length; i++) {
			var num_msgs = data.archives[i].num_msgs.toString();
	        // var time = new Date(0);
	        // time.setUTCSeconds(data.archives[i].latest);
	        // latest = time.getFullYear() + '-' + zfill(time.getMonth() + 1, 2) + '-' + zfill(time.getDate(), 2) + ' ' + zfill(time.getHours(), 2) + ':' + zfill(time.getMinutes(), 2) + ':' + zfill(time.getSeconds(), 2);
			if (data.archives[i].has_more) { num_msgs = num_msgs + '+'}
			html += '<tr class="active"><td><span class="pull-right"><span class="label label-default">' + data.archives[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-ban-circle"></span></td><td><span class="pull-right">' + data.archives[i].num_members + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + num_msgs + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + data.archives[i].num_files + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="label label-primary">' + data.archives[i].latest + '</span></td></tr>';
		}
		html += '<tr><td colspan="5" style="padding: 0px;"></td></tr>';
		$("#table_slack_channel").html(html);

        $("#id_channel_num > div > div.progress-bar-success").css("width", (data.channels.length / (data.archives.length + data.channels.length) * 100).toString() + '%' ).html(data.channels.length);
        $("#id_channel_num > div > div.progress-bar-danger").css("width", (data.archives.length / (data.archives.length + data.channels.length) * 100).toString() + '%' ).html(data.archives.length);
    }
});

$.ajax({
    url : "/admin/slack_dash?qs=files&tqx=reqId%3A54",
    dataType: "json",
    success: function (data) {
		var html = "";
		for (var i = 0; i < data.files.types.length; i++) {
			html += '<tr><td><span class="pull-right"><code>' + data.files.types[i] + '</code></span></td><td><span class="pull-right">' + data.files.nums[i] + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#00f;">' + formatSizeUnits(data.files.sizes[i]) + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td></tr>';
		}
		html += '<tr><td colspan="3" style="padding: 0px;"></td></tr>';
		$("#table_slack_file").html(html);

        $("#num_file").html('<span class="pull-right">' + data.files.nums[0] + '&nbsp;&nbsp;&nbsp;&nbsp;</span>');
        $("#size_file").html('<span class="pull-right" style="color:#00f;">' + formatSizeUnits(data.files.sizes[0]) + '&nbsp;&nbsp;&nbsp;&nbsp;</span>');
    }
});


var chart = new google.visualization.ChartWrapper({
	'chartType': 'AreaChart',
	'dataSourceUrl': '/admin/slack_dash?qs=plot_msgs',
	'containerId': 'plot_slack_msgs',
    'options': {
        'chartArea': {'width': '90%', 'left': '10%'},
        'legend': {'position': 'none'},
        'title': 'Last 7 Days',
        'titleTextStyle': {'bold': false, 'fontSize': 16},
        'vAxis': {
            'title': '(#)',
            'titleTextStyle': {'bold': true},
        },
        'hAxis': {
            'gridlines': {'count': -1},
            'textStyle': {'italic': true},
            'format': 'MMM dd'
        },
        'lineWidth': 3,
        'pointSize': 5,
        'colors': ['#50cc32'],
        'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
    }
});
google.visualization.events.addListener(chart, 'ready', readyHandler);
chart.draw();

var chart = new google.visualization.ChartWrapper({
	'chartType': 'AreaChart',
	'dataSourceUrl': '/admin/slack_dash?qs=plot_files',
	'containerId': 'plot_slack_files',
    'options': {
        'chartArea': {'width': '90%', 'left': '10%'},
        'legend': {'position': 'none'},
        'title': 'Last 7 Days',
        'titleTextStyle': {'bold': false, 'fontSize': 16},
        'vAxis': {
            'title': '(#)',
            'titleTextStyle': {'bold': true},
        },
        'hAxis': {
            'gridlines': {'count': -1},
            'textStyle': {'italic': true},
            'format': 'MMM dd'
        },
        'lineWidth': 3,
        'pointSize': 5,
        'colors': ['#ff69bc'],
        'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
    }
});
google.visualization.events.addListener(chart, 'ready', readyHandler);
chart.draw();

