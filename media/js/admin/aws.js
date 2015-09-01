google.load('visualization', '1.1', {packages: ['corechart']});
google.setOnLoadCallback(drawDash);

function drawDash() {
	var lineOptions = { };

   	google.visualization.drawChart({
    	'chartType': 'ColumnChart',
    	'dataSourceUrl': '/admin/aws_stat?qs=latency&sp=48h',
    	'containerId': 'plot_lat1',
    	'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'Last 48 Hours',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Milliseconds (ms)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true}
            },
            'bar': {'groupWidth': '500%' },
            'colors': ['#8ee4cf'],
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=latency&sp=7d',
        'containerId': 'plot_lat2',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Milliseconds (ms)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#8ee4cf'],
        }
    });

    google.visualization.drawChart({
        'chartType': 'ColumnChart',
        'dataSourceUrl': '/admin/aws_stat?qs=request&sp=48h',
        'containerId': 'plot_req1',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'Last 48 Hours',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Count (#)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true}
            },
            'bar': {'groupWidth': '500%' },
            'colors': ['#5496d7'],
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=request&sp=7d',
        'containerId': 'plot_req2',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Count (#)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#5496d7'],
        }
    });

    google.visualization.drawChart({
        'chartType': 'ColumnChart',
        'dataSourceUrl': '/admin/aws_stat?qs=cpu&sp=48h',
        'containerId': 'plot_cpu1',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'Last 48 Hours',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Percent (%)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true}
            },
            'bar': {'groupWidth': '500%' },
            'colors': ['#c28fdd'],
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=cpu&sp=7d',
        'containerId': 'plot_cpu2',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Percent (%)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#c28fdd'],
        }
    });

    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=host&sp=7d',
        'containerId': 'plot_host',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Count (#)',
                'titleTextStyle': {'bold': true},
                'viewWindow': {'max': 2, 'min': 0},
                'ticks': [0, 1, 2]
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#50cc32', '#ff69bc'],
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=credit&sp=7d',
        'containerId': 'plot_credit',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Count (#)',
                'titleTextStyle': {'bold': true},
                'viewWindow': {'min': 0},
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#ff5c2b', '#29be92'],
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=status&sp=7d',
        'containerId': 'plot_status',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Count (#)',
                'titleTextStyle': {'bold': true},
                'viewWindow': {'min': 0}
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#ff5c2b', '#ff69bc', '#ff912e'],
        }
    });

    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=network&sp=7d',
        'containerId': 'plot_net',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Kilobytes/Second (kb/s)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#ff912e', '#3ed4e7'],
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=volbytes&sp=7d',
        'containerId': 'plot_vol',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Kilobytes/Second (kb/s)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#ff912e', '#3ed4e7'],
        }
    });

    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=23xx&sp=7d',
        'containerId': 'plot_23xx',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Count (#)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#5496d7', '#29be92'],
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_stat?qs=45xx&sp=7d',
        'containerId': 'plot_45xx',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': 'Count (#)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': 7},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#c28fdd', '#ff5c2b'],
        }
    });
	setTimeout(function() {$(".place_holder").removeClass("place_holder");}, 1000);
}


