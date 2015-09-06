google.load('visualization', '1.1', {packages: ['corechart']});

function drawEC2(id) {
   	google.visualization.drawChart({
    	'chartType': 'AreaChart',
    	'dataSourceUrl': '/admin/aws_dash?qs=cpu&tp=ec2&id=' + id,
    	'containerId': 'plot_cpu_' + id,
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'CPU Utilization',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': '(%)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true}
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#29be92'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_dash?qs=net&tp=ec2&id=' + id,
        'containerId': 'plot_net_'+ id,
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Network I/O',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': '(kb/s)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true}
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#ff912e', '#3ed4e7'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });
}


function drawELB(id) {
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_dash?qs=lat&tp=elb&id=' + id,
        'containerId': 'plot_lat_' + id,
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'Latency',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': '(ms)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true}
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#8ee4cf'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_dash?qs=req&tp=elb&id=' + id,
        'containerId': 'plot_req_'+ id,
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'HTTP Requests',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': '(#)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true}
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#5496d7'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });
}


function drawEBS(id) {
    google.visualization.drawChart({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/aws_dash?qs=disk&tp=ebs&id=' + id,
        'containerId': 'plot_disk_' + id,
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Disk I/O',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': '(kb/s)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true},
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#ff912e', '#3ed4e7'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });
}

