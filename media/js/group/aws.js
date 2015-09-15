google.load('visualization', '1', {packages: ['corechart']});
google.setOnLoadCallback(drawChart);
var gviz_handles = [];

function readyHandler() {
    $(".place_holder").each(function() {
        if ($(this).html().length > 0) { $(this).removeClass("place_holder"); }
    });
}


function drawEC2(id) {
   	var chart = new google.visualization.ChartWrapper({
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
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();
    gviz_handles.push(chart);

    var chart = new google.visualization.ChartWrapper({
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
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();
    gviz_handles.push(chart);
}


function drawELB(id) {
    var chart = new google.visualization.ChartWrapper({
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
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();
    gviz_handles.push(chart);

    var chart = new google.visualization.ChartWrapper({
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
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();
    gviz_handles.push(chart);
}


function drawEBS(id) {
    var chart = new google.visualization.ChartWrapper({
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
    google.visualization.events.addListener(chart, 'ready', readyHandler);
    chart.draw();
    gviz_handles.push(chart);
}


function drawChart() {
    $.ajax({
        url : "/admin/aws_dash?qs=init&id=init&tp=init&tqx=reqId%3A55",
        dataType: "json",
        success: function (data) {
            var html = "";
            for (var i = 0; i < data.table.length; i++) {
                var ec2 = "", elb = "", ebs = "";
                if (!data.table[i].hasOwnProperty('ec2')) { data.table[i]['ec2'] = {'id':'', 'status':-1, 'name':''}; }
                if (!data.table[i].hasOwnProperty('elb')) { data.table[i]['elb'] = {'id':'', 'status':false, 'name':''}; }
                if (!data.table[i].hasOwnProperty('ebs')) { data.table[i]['ebs'] = {'id':'', 'status':-1, 'name':''}; }
                if (data.table[i].ec2.status == 0) {
                    ec2 = '<span class="pull-left"><span class="label label-warning"><span class="glyphicon glyphicon-question-sign"></span></span></span>';
                } else if (data.table[i].ec2.status == 16) {
                    ec2 = '<span class="pull-left"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                } else if (data.table[i].ec2.status == 48 || data.table[i].ec2.status == 80) {
                    ec2 = '<span class="pull-left"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                } else if (data.table[i].ec2.status == 32 || data.table[i].ec2.status == 64) {
                    ec2 = '<span class="pull-left"><span class="label label-magenta"><span class="glyphicon glyphicon-exclamation-sign"></span></span></span>';
                }
                if (data.table[i].elb.status) {
                    elb = '<span class="pull-left"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                } else if (data.table[i].elb.name.length > 0) {
                    elb = '<span class="pull-left"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                }
                if (data.table[i].ebs.status == 'in-use') {
                    ebs = '<span class="pull-left"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                } else if (data.table[i].ebs.name.length > 0) {
                    ebs = '<span class="pull-left"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                }
                html += '<tr><td>' + ec2 + '&nbsp;&nbsp;<span class="label label-orange">' + data.table[i].ec2.id + '</span>&nbsp;&nbsp;<u><a href="#ec2-' + data.table[i].ec2.name + '" id="aws_ec2-' + data.table[i].ec2.name + '">' + data.table[i].ec2.name + '</a></u></td><td>' + elb + '&nbsp;&nbsp;<u><a href="#elb' + data.table[i].elb.name + '" id="aws_elb-' + data.table[i].elb.name + '">' + data.table[i].elb.name + '</a></u></td><td>' + ebs + '&nbsp;&nbsp;<span class="label label-orange">' + data.table[i].ebs.id + '</span>&nbsp;&nbsp;<u><a href="#ebs-' + data.table[i].ebs.name + '" id="aws_ebs-' + data.table[i].ebs.name + '">' + data.table[i].ebs.name + '</a></u></td></tr>';
            }
            html += '<tr><td colspan="3" style="padding: 0px;"></td></tr>';
            $("#aws_table_body").html(html).removeClass("place_holder");

            setTimeout(function() {
                var html = "";
                for (var i = 0; i < data.ec2.length; i++) {
                    var ec2 = "";
                    if (data.ec2[i].status == 0) {
                        ec2 = '<span class="pull-left"><span class="label label-warning"><span class="glyphicon glyphicon-question-sign"></span></span></span>';
                    } else if (data.ec2[i].status == 16) {
                        ec2 = '<span class="pull-left"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                    } else if (data.ec2[i].status == 48 || data.ec2[i].status == 80) {
                        ec2 = '<span class="pull-left"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                    } else if (data.ec2[i].status == 32 || data.ec2[i].status == 64) {
                        ec2 = '<span class="pull-left"><span class="label label-magenta"><span class="glyphicon glyphicon-exclamation-sign"></span></span></span>';
                    }
                    html += '<div class="row" id="ec2-' + data.ec2[i].name + '"><div class="col-md-9"><p><span class="lead">' + ec2 + '&nbsp;&nbsp;<b><u>' + data.ec2[i].name + '</u></b></span>&nbsp;&nbsp;<span class="label label-orange">' + data.ec2[i].id + '</span>&nbsp;<span class="label label-primary">' + data.ec2[i].type + '</span>&nbsp;<span class="label label-info">' + data.ec2[i].arch + '</span>&nbsp;<span class="label label-violet">' + data.ec2[i].region + '</span></p><p><a href="http://' + data.ec2[i].dns + '" target="_blank"><code>' + data.ec2[i].dns + '</code></a></p></div><div class="col-md-3"><p class="text-right"><span class="label label-inverse">Credits Balance</span></p><p class="text-right"><i><mark>' + data.ec2[i].credit + '</mark></i></p></div></div><div class="row"><div class="col-md-6"><div id="plot_cpu_' + data.ec2[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 120px;"></div></div><div class="col-md-6"><div id="plot_net_' + data.ec2[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 120px;"></div></div></div>';
                    if (i != data.ec2.length - 1) {
                        html += '<hr/ style="margin: 10px;">';
                    }
                }
                $("#aws_ec2_body").html(html).removeClass("place_holder");
                for (var i = 0; i < data.ec2.length; i++) {
                    drawEC2(data.ec2[i].id);
                }
            }, 500);

            setTimeout(function() {
                var html = "";
                for (var i = 0; i < data.elb.length; i++) {
                    var elb = "";
                    if (data.elb[i].status) {
                        elb = '<span class="pull-left"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                    } else if (data.elb[i].name.length > 0) {
                        elb = '<span class="pull-left"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                    }
                    html += '<div class="row" id="elb-' + data.elb[i].name + '"><div class="col-md-12"><p><span class="lead">' + elb + '&nbsp;&nbsp;<b><u>' + data.elb[i].name + '</u></b></span>&nbsp;&nbsp;<span class="label label-orange">' + data.ec2[i].id + '</span>&nbsp;<span class="label label-primary">' + data.ec2[i].type + '</span>&nbsp;<span class="label label-info">' + data.ec2[i].arch + '</span>&nbsp;<span class="label label-violet">' + data.elb[i].region + '</span></p><p><a href="http://' + data.elb[i].dns + '" target="_blank"><code>' + data.elb[i].dns + '</code></a></p></div></div><div class="row"><div class="col-md-6"><div id="plot_lat_' + data.elb[i].name + '" class="thumbnail place_holder" style="padding:0px 20px; height: 120px;"></div></div><div class="col-md-6"><div id="plot_req_' + data.elb[i].name + '" class="thumbnail place_holder" style="padding:0px 20px; height: 120px;"></div></div></div>';
                    if (i != data.elb.length - 1) {
                        html += '<hr/ style="margin: 10px;">';
                    }
                }
                $("#aws_elb_body").html(html).removeClass("place_holder");
                for (var i = 0; i < data.elb.length; i++) {
                    drawELB(data.elb[i].name);
                }
            }, 1000);

            setTimeout(function() {
                var html = "";
                for (var i = 0; i < data.ebs.length; i++) {
                    var ebs = "", encrpyed = "";
                    if (data.ebs[i].status == 'in-use') {
                        ebs = '<span class="pull-left"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                    } else if (data.ebs[i].name.length > 0) {
                        ebs = '<span class="pull-left"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                    }
                    if (data.ebs[i].encrypted) { encrpyed = '&nbsp;<span class="label label-warning">Encrypted</span>'; }
                    html += '<div class="row" id="ebs-' + data.ebs[i].name + '"><div class="col-md-4"><p><span class="lead">' + ebs + '&nbsp;&nbsp;<b><u>' + data.ebs[i].name + '</u></b></span>&nbsp;&nbsp;</p><p><span class="label label-orange">' + data.ebs[i].id + '</span>&nbsp;<span class="label label-primary">' + data.ebs[i].type + '</span>&nbsp;<span class="label label-info">' + data.ebs[i].size + ' GB</span>&nbsp;<span class="label label-violet">' + data.ebs[i].region + '</span>' + encrpyed + '</p></div><div class="col-md-8"><div id="plot_disk_' + data.ebs[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 120px;"></div></div></div>'
                    if (i != data.ebs.length - 1) {
                        html += '<hr/ style="margin: 10px;">';
                    }
                }
                $("#aws_ebs_body").html(html).removeClass("place_holder");
                for (var i = 0; i < data.ebs.length; i++) {
                    drawEBS(data.ebs[i].id);
                }
            }, 1500);

        }
    });
}


$(window).on("resize", function() {
    clearTimeout($.data(this, 'resizeTimer'));
    $.data(this, 'resizeTimer', setTimeout(function() {
        for (var i = 0; i < gviz_handles.length; i++) {
            gviz_handles[i].draw();
        }
    }, 200));
});


