(function(w,d,s,g,js,fs){
	g=w.gapi||(w.gapi={});g.analytics={q:[],ready:function(f){this.q.push(f);}};
	js=d.createElement(s);fs=d.getElementsByTagName(s)[0];
	js.src='https://apis.google.com/js/platform.js';
	fs.parentNode.insertBefore(js,fs);js.onload=function(){g.load('analytics');};
}(window,document,'script'));

gapi.analytics.ready(function() {

	gapi.analytics.auth.authorize({
		'container': 'embed-api-auth-container',
		'clientid': client_id,
		'serverAuth': { 'access_token': access_token }
	});

	var viewSelector = new gapi.analytics.ViewSelector({ 'container': 'view-selector-container' });
	viewSelector.execute();

	var chart_24h = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:sessions',
			'dimensions': 'ga:dateHour',
			'start-date': 'yesterday',
			'end-date': 'today'
		},
		'chart': {
			'container': 'chart_24h',
			'type': 'LINE',
			'options': {
				'width': '100%',
				'height': '25%',
				'title': 'Last 24 Hours',
				'colors': ['#c28fdd'],
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});
	var chart_7d = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:sessions',
			'dimensions': 'ga:date',
			'start-date': '7daysAgo',
			'end-date': 'today'
		},
		'chart': {
			'container': 'chart_7d',
			'type': 'LINE',
			'options': {
				'width': '100%',
				'height': '25%',
				'title': 'Last 7 Days',
				'colors': ['#d86f5c'],
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});
	var chart_1m = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:sessions',
			'dimensions': 'ga:date',
			'start-date': '30daysAgo',
			'end-date': 'yesterday'
		},
		'chart': {
			'container': 'chart_1m',
			'type': 'LINE',
			'options': {
				'width': '100%',
				'height': '25%',
				'title': 'Last 30 Days',
				'colors': ['#ff912e'],
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});
	var chart_3m = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:sessions',
			'dimensions': 'ga:date',
			'start-date': '90daysAgo',
			'end-date': 'yesterday'
		},
		'chart': {
			'container': 'chart_3m',
			'type': 'LINE',
			'options': {
				'width': '100%',
				'height': '25%',
				'title': 'Last 90 Days',
				'colors': ['#29be92'],
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});
	var geo_session = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:sessions',
			'dimensions': 'ga:country',
			'start-date': '30daysAgo',
			'end-date': 'yesterday'
		},
		'chart': {
			'container': 'geo_session',
			'type': 'GEO',
			'options': {
				'width': '100%',
				'title': 'Sessions',
				'colorAxis': {'colors': ['#ddf6f0','#5496d7']},
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});
	var pie_session = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:sessions',
			'dimensions': 'ga:userType',
			'start-date': '30daysAgo',
			'end-date': 'yesterday'
		},
		'chart': {
			'container': 'pie_session',
			'type': 'PIE',
			'options': {
				'width': '100%',
				'title': 'Sessions',
				'legend': {'position': 'bottom'},
				'colors': ['#50cc32', '#ff69bc'],
				'pieHole': 0.33,
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});
	var pie_user = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:users',
			'dimensions': 'ga:userType',
			'start-date': '30daysAgo',
			'end-date': 'yesterday'
		},
		'chart': {
			'container': 'pie_user',
			'type': 'PIE',
			'options': {
				'width': '100%',
				'title': 'Visitors',
				'legend': {'position': 'bottom'},
				'colors': ['#3ed4e7', '#ff912e'],
				'pieHole': 0.33,
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});
	var pie_browser = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:users',
			'dimensions': 'ga:browser',
			'start-date': '30daysAgo',
			'end-date': 'yesterday',
			'filters': 'ga:browser=@Firefox,ga:browser=@Chrome,ga:browser=@Safari,ga:browser=@Internet Explorer',
			'sort': 'ga:browser',
			'max-results': 4,
		},
		'chart': {
			'container': 'pie_browser',
			'type': 'PIE',
			'options': {
				'width': '100%',
				'title': 'Browser',
				'legend': {'position': 'bottom', 'maxLines': 2},
				'colors': ['#29be92', '#ff912e', '#5496d7', '#ff5c2b'],
				'pieHole': 0.33,
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});
	var pie_pageview = new gapi.analytics.googleCharts.DataChart({
		'query': {
			'metrics': 'ga:pageviews',
			'dimensions': 'ga:userType',
			'start-date': '30daysAgo',
			'end-date': 'yesterday',
		},
		'chart': {
			'container': 'pie_pageview',
			'type': 'PIE',
			'options': {
				'width': '100%',
				'title': 'Page Views',
				'legend': {'position': 'bottom'},
				'colors': ['#8ee4cf', '#c28fdd'],
				'pieHole': 0.33,
            	'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
			}
		}
	});

	viewSelector.on('change', function(ids) {
		chart_24h.set({'query': {'ids': ids}}).execute();
		chart_7d.set({'query': {'ids': ids}}).execute();
		chart_1m.set({'query': {'ids': ids}}).execute();
		chart_3m.set({'query': {'ids': ids}}).execute();
		geo_session.set({'query': {'ids': ids}}).execute();
		pie_session.set({'query': {'ids': ids}}).execute();
		pie_user.set({'query': {'ids': ids}}).execute();
		pie_browser.set({'query': {'ids': ids}}).execute();
		pie_pageview.set({'query': {'ids': ids}}).execute();
	});

	setTimeout(function() {$(".place_holder").removeClass("place_holder");}, 800);

});


