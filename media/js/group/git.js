google.load('visualization', '1.1', {packages: ['corechart']});

function readyHandler() {
    $(".place_holder").each(function() {
        if ($(this).html().length > 0) { $(this).removeClass("place_holder"); }
    });
}

function drawGIT(repo) {
    var chart = new google.visualization.ChartWrapper({
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
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();

    var chart = new google.visualization.ChartWrapper({
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
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();
}


$.ajax({
    url : "/admin/git_dash?qs=init&repo=init&tqx=reqId%3A55",
    dataType: "json",
    success : function (data) {
        var html = "";
        for (var i = 0; i < data.git.length; i++) {
            var lb_private = "";
            if (data.git[i].private) {
                lb_private = '<span class="label label-primary">private</span>';
            } else {
                lb_private = '<span class="label label-magenta">public</span>';
            }

            html += '<div class="row"><div class="col-md-6"><p><span class="lead"><mark><b><u>' + data.git[i].id + '</u></b></mark></span>&nbsp;&nbsp;' + lb_private + '</p><p><a href="http://' + data.git[i].url + '" target="_blank"><code>' + data.git[i].url + '</code></a></p><table class="table"><thead><tr class="active"><th class="col-md-3"><span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Account</th><th class="col-md-3"><span class="glyphicon glyphicon-circle-arrow-up"></span>&nbsp;&nbsp;Commits</th><th class="col-md-3"><span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;Additions</th><th class="col-md-3"><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;Deletions</th></tr></thead><tbody>';

            for (var j = 0; j < data.git[i].data.length; j++) {
                html += '<tr><td>' + data.git[i].data[j].Contributors + '</td><td><span class="pull-right" style="color:#00f;">' + data.git[i].data[j].Commits + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#080;">' + data.git[i].data[j].Additions + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#f00;">' + data.git[i].data[j].Deletions + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td></tr>';
            }
            html += '<tr><td colspan="4" style="padding: 0px;"></td></tr></tbody></table></div><div class="col-md-6"><div id="plot_c_' + data.git[i].name + '" class="thumbnail git place_holder" style="padding:0px 20px; height: 120px;"></div><div id="plot_ad_' + data.git[i].name + '" class="thumbnail git place_holder" style="padding:0px 20px; height: 120px;"></div></div></div>';
            if (i == data.git.length - 1) {
                html += '<hr/ style="margin: 10px;">';
            }
        }
        $("#git_body").html(html).removeClass("place_holder");

        for (var i = 0; i < data.git.length; i++) {
            drawGIT(data.git[i].name);
        }
    }
});

