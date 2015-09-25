google.load('visualization', '1', {packages: ['corechart']});
google.setOnLoadCallback(drawChart);
var gviz_handles = [];

function readyHandler() {
    $(".place_holder").each(function() {
        if ($(this).html().length > 0) { $(this).removeClass("place_holder"); }
    });
}

function drawGIT(repo) {
    var chart = new google.visualization.ChartWrapper({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/group/git_dash?qs=c&repo=' + repo,
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
    gviz_handles.push(chart);

    var chart = new google.visualization.ChartWrapper({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/group/git_dash?qs=ad&repo=' + repo,
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
    gviz_handles.push(chart);
}


function drawChart() {
    $.ajax({
        url : "/group/git_dash?qs=init&repo=init&tqx=reqId%3A55",
        dataType: "json",
        success: function (data) {
            var html = "";
            for (var i = 0; i < data.git.length; i++) {
                var lb_private = "";
                if (data.git[i].private) {
                    lb_private = '<span class="label label-success">private</span>';
                } else {
                    lb_private = '<span class="label label-magenta">public</span>';
                }

                html += '<div class="row"><div class="col-lg-6 col-md-6 col-sm-6 col-xs-6"><p><span class="lead"><mark><b><u>' + data.git[i].id + '</u></b></mark></span>&nbsp;&nbsp;' + lb_private + '</p><p><a href="http://' + data.git[i].url + '" target="_blank"><code>' + data.git[i].url + '</code></a></p><p id="git-label-' + data.git[i].name + '"></p><table class="table table-hover"><thead><tr class="active"><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Account</th><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-circle-arrow-up"></span>&nbsp;&nbsp;Commits</th><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;Additions</th><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;Deletions</th></tr></thead><tbody>';

                for (var j = 0; j < data.git[i].data.length; j++) {
                    html += '<tr><td>' + data.git[i].data[j].Contributors + '</td><td><span class="pull-right" style="color:#00f;">' + data.git[i].data[j].Commits + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#080;">' + data.git[i].data[j].Additions + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#f00;">' + data.git[i].data[j].Deletions + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td></tr>';
                }
                html += '<tr><td colspan="4" style="padding: 0px;"></td></tr></tbody></table></div><div class="col-lg-6 col-md-6 col-sm-6 col-xs-6"><div id="plot_c_' + data.git[i].name + '" class="thumbnail git place_holder" style="padding:0px 20px; height: 150px;"></div><div id="plot_ad_' + data.git[i].name + '" class="thumbnail git place_holder" style="padding:0px 20px; height: 150px;"></div></div></div>';
                if (i != data.git.length - 1) {
                    html += '<hr/ style="margin: 10px;">';
                }
            }
            $("#git_body").html(html).removeClass("place_holder");

            for (var i = 0; i < data.git.length; i++) {
                var name = data.git[i].name;
                drawGIT(name);
                $.ajax({
                    url : "/group/git_dash?qs=num&repo=" + name + "&tqx=reqId%3A55",
                    dataType: "json",
                    success: function (data) {
                        $("#git-label-" + data.name).html('<span class="label label-green">created</span>&nbsp;<span class="label label-primary">' + data.created_at + '</span>&nbsp;&nbsp;<span class="label label-dark-green">last pushed</span>&nbsp;<span class="label label-primary">' + data.pushed_at + '</span></p><p><span class="label label-danger">issue</span>&nbsp;' + data.num_issues + '&nbsp;&nbsp;<span class="label label-info">download</span>&nbsp;' + data.num_downloads + '&nbsp;&nbsp;<span class="label label-info">pull</span>&nbsp;' + data.num_pulls + '&nbsp;&nbsp;<span class="label label-orange">branch</span>&nbsp;' + data.num_branches + '&nbsp;&nbsp;<span class="label label-orange">fork</span>&nbsp;' + data.num_forks + '&nbsp;&nbsp;<span class="label label-violet">watcher</span>&nbsp;' + data.num_watchers);
                    }
                });
            }
        }
    });
}


$(window).on("resize", function() {
    clearTimeout($(window).data(this, 'resizeTimer'));
    $(window).data(this, 'resizeTimer', setTimeout(function() {
        for (var i = 0; i < gviz_handles.length; i++) {
            gviz_handles[i].draw();
        }
    }, 200));
});


