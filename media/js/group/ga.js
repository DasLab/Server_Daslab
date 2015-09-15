(function(w,d,s,g,js,fs){
	g=w.gapi||(w.gapi={});g.analytics={q:[],ready:function(f){this.q.push(f);}};
	js=d.createElement(s);fs=d.getElementsByTagName(s)[0];
	js.src='https://apis.google.com/js/platform.js';
	fs.parentNode.insertBefore(js,fs);js.onload=function(){g.load('analytics');};
}(window,document,'script'));


function readyHandler() {
    $(".place_holder").each(function() {
        if ($(this).html().length > 0) { $(this).removeClass("place_holder"); }
    });
}


function drawGA(id) {
	new gapi.analytics.googleCharts.DataChart({
		'query': {
			'ids': 'ga:' + id,
			'metrics': 'ga:sessions',
			'dimensions': 'ga:date',
			'start-date': '30daysAgo',
			'end-date': 'yesterday'
		},
		'chart': {
			'container': 'chart_session_' + id,
			'type': 'LINE',
			'options': {
				'width': '100%',
				'height': '25%',
				'title': 'Last 30 Days',
				'colors': ['#c28fdd'],
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	}).once('success', readyHandler).execute();

	new gapi.analytics.googleCharts.DataChart({
		'query': {
			'ids': 'ga:' + id,
			'metrics': 'ga:percentNewSessions',
			'dimensions': 'ga:date',
			'start-date': '30daysAgo',
			'end-date': 'yesterday'
		},
		'chart': {
			'container': 'chart_visitor_' + id,
			'type': 'LINE',
			'options': {
				'width': '100%',
				'height': '25%',
				'title': 'Last 30 Days',
				'colors': ['#ff5c2b'],
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	}).once('success', readyHandler).execute();
}


$("#view-selector-container").hide();

gapi.analytics.ready(function() {
	$.ajax({
	    url : "/admin/ga_dash",
	    dataType: "json",
	    success: function (data) {
			gapi.analytics.auth.authorize({
				'container': 'embed-api-auth-container',
				'clientid': data.client_id,
				'serverAuth': { 'access_token': data.access_token }
			});
			new gapi.analytics.ViewSelector({ 'container': 'view-selector-container' }).execute();

			var html = "";
			for (var i = 0; i < data.projs.length; i++) {
                var ga = "";
                if (data.projs[i].name.length > 0) {
                    ga = '<span class="pull-left lead"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                } else {
                    ga = '<span class="pull-left lead"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                }
				html += '<div class="row"><p><span class="lead">' + ga + '&nbsp;&nbsp;<b><u>' + data.projs[i].name + '</u></b></span>&nbsp;&nbsp;<span class="label label-primary">' + data.projs[i].track_id + '</span><span class="pull-right"><span class="label label-warning">Bounce Rate</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].bounceRate + ' %</span>&nbsp;&nbsp;<span class="label label-orange">Users</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].users + '</span></span></p><p><a href="' + data.projs[i].url + '" target="_blank"><code>' + data.projs[i].url + '</code></a><span class="pull-right"><span class="label label-success">Sessions</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].sessions + '</span>&nbsp;&nbsp;<span class="label label-success">Session Duration</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].sessionDuration + '</span>&nbsp;&nbsp;<span class="label label-info">Page Views</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].pageviews + '</span>&nbsp;&nbsp;<span class="label label-info">Page View / Session</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].pageviewsPerSession + '</span></span></p></div><div class="row"><div class="col-md-6"><div id="chart_session_' + data.projs[i].id + '" class="thumbnail place_holder" style="padding:0px 20px;"></div></div><div class="col-md-6"><div id="chart_visitor_' + data.projs[i].id + '" class="thumbnail place_holder" style="padding:0px 20px;"></div></div></div>';
                if (i != data.projs.length - 1) {
                    html += '<hr/ style="margin: 10px;">';
                }
			}
            $("#ga_body").html(html).removeClass("place_holder");
			for (var i = 0; i < data.projs.length; i++) {
				drawGA(data.projs[i].id);
			}
	    },
	    complete: function () {
		    $("#sidebar").attr("data-spy","affix").affix( { offset: { top: $("#main").position().top} } );
	    	$("#sidebar").css("width", $("#sidebar").width());
	    	$("#sidebar").css("margin", 0);
	    }
	});
});


