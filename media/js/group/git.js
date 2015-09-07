google.load('visualization', '1.1', {packages: ['corechart']});
google.setOnLoadCallback(drawDash);

function drawGIT(repo) {
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/git_dash?qs=c&repo=' + repo,
        'containerId': 'plot_c_' + repo,
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
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
            'lineWidth': 2,
            'pointSize': 3,
            'colors': ['#3ed4e7'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });

    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/git_dash?qs=ad&repo=' + repo,
        'containerId': 'plot_ad_' + repo,
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
            'lineWidth': 2,
            'pointSize': 3,
            'colors': ['#29be92', '#ff5c2b'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });
}


