google.load('visualization', '1.1', {packages: ['corechart', 'calendar']});
google.setOnLoadCallback(drawDash);

function drawDash() {

    google.visualization.drawChart({
        'chartType': 'Calendar',
        'dataSourceUrl': '/admin/git_stat?qs=c',
        'containerId': 'plot_c',
        'options': {
            'title': 'Last Year',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'calendar': {
                'cellColor': {'stroke': '#fff'},
                'underYearSpace': 20,
                'yearLabel': {'color': '#c28fdd', 'bold': true},
                'monthLabel': {'color': '#000'},
                'monthOutlineColor': {'stroke': '#d86f5c', 'strokeOpacity': 0.8, 'strokeWidth': 2},
                'dayOfWeekLabel': {'color': '#000'}
            },
            'colorAxis': { 'minValue': 0, 'colors': ['#e8f9f5', '#5496d7']},
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });

    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/git_stat?qs=ad',
        'containerId': 'plot_ad',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Weekly Aggregation',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Count (#)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#29be92', '#ff5c2b'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });

    google.visualization.drawChart({
        'chartType': 'PieChart',
        'dataSourceUrl': '/admin/git_stat?qs=au',
        'containerId': 'plot_pie',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Contributors Commits',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'pieHole': 0.33,
            'colors': ['#3ed4e7', '#ff912e', '#29be92', '#ff5c2b'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });

	setTimeout(function() {$(".place_holder").removeClass("place_holder");}, 800);
}


