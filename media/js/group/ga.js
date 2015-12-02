google.load('visualization', '1', {packages: ['corechart']});
google.setOnLoadCallback(drawChart);
var gviz_handles = [];

function readyHandler() {
    $(".place_holder").each(function() {
        if ($(this).html().length > 0) { $(this).removeClass("place_holder"); }
    });
}


function drawGA(id) {
    var chart = new google.visualization.ChartWrapper({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/group/ga_dash/?qs=sessions&id=' + id,
        'containerId': 'chart_session_' + id,
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 30 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': '(#)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'showTextEvery': 2,
                'gridlines': {'count': -1},
                'textStyle': {'italic': true}
            },
            'lineWidth': 3,
            'pointSize': 5,
            'colors': ['#c28fdd'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();
    gviz_handles.push(chart);

    var chart = new google.visualization.ChartWrapper({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/group/ga_dash/?qs=percentNewSessions&id=' + id,
        'containerId': 'chart_visitor_' + id,
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'bottom'},
            'title': 'Last 30 Days',
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
            'colors': ['#ff5c2b'],
            'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
        }
    });
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();
    gviz_handles.push(chart);
}


function drawChart() {
    $.ajax({
        url : "/group/ga_dash/?qs=init&id=init&tqx=reqId%3A55",
        dataType: "json",
        success: function (data) {
            var html = "";
            for (var i = 0; i < data.projs.length; i++) {
                var ga = "";
                if (data.projs[i].name.length > 0) {
                    ga = '<span class="pull-left lead"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                } else {
                    ga = '<span class="pull-left lead"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                }
                html += '<div class="row"><p><span class="lead">' + ga + '&nbsp;&nbsp;<b><u>' + data.projs[i].name + '</u></b></span>&nbsp;&nbsp;<span class="label label-primary">' + data.projs[i].track_id + '</span><span class="pull-right"><span class="label label-warning">Bounce Rate</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].bounceRate + ' %</span>&nbsp;&nbsp;<span class="label label-orange">Users</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].users + '</span></span></p><p><a href="' + data.projs[i].url + '" target="_blank"><code>' + data.projs[i].url + '</code></a><span class="pull-right"><span class="label label-success">Sessions</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].sessions + '</span>&nbsp;&nbsp;<span class="label label-success">Session Duration</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].sessionDuration + '</span>&nbsp;&nbsp;<span class="label label-info">Page Views</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].pageviews + '</span>&nbsp;&nbsp;<span class="label label-info">Page View / Session</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].pageviewsPerSession + '</span></span></p></div><div class="row"><div class="col-lg-6 col-md-6 col-sm-6 col-xs-6"><div id="chart_session_' + data.projs[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div><div class="col-lg-6 col-md-6 col-sm-6 col-xs-6"><div id="chart_visitor_' + data.projs[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div></div>';
                if (i != data.projs.length - 1) {
                    html += '<hr/ style="margin: 10px;">';
                }
            }
            $("#ga_body").html(html).removeClass("place_holder");
            for (var i = 0; i < data.projs.length; i++) {
                drawGA(data.projs[i].id);
            }
        },
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


