(function(w,d,s,g,js,fs){
	g=w.gapi||(w.gapi={});g.analytics={q:[],ready:function(f){this.q.push(f);}};
	js=d.createElement(s);fs=d.getElementsByTagName(s)[0];
	js.src='https://apis.google.com/js/platform.js';
	fs.parentNode.insertBefore(js,fs);js.onload=function(){g.load('analytics');};
}(window,document,'script'));


$("#view-selector-container").hide();
setTimeout(function() {$(".place_holder").removeClass("place_holder");}, 1000);


function drawSVG(id) {
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
	}).execute();
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
	}).execute();
}

