google.load('visualization', '1', {packages: ['corechart']});
google.setOnLoadCallback(drawChart);
var gviz_handles = [];

function formatSizeUnits(bytes){
    if      (bytes >= 1000000000) {bytes = (bytes / 1000000000).toFixed(2) + ' GB';}
    else if (bytes >= 1000000)    {bytes = (bytes / 1000000).toFixed(2) + ' MB';}
    else if (bytes >= 1000)       {bytes = (bytes / 1000).toFixed(2) + ' KB';}
    else if (bytes > 1)           {bytes = bytes + ' bytes';}
    else if (bytes == 1)          {bytes = bytes + ' byte';}
    else                          {bytes = '0 byte';}
    return bytes;
}

function readyHandler() {
    $(".place_holder").each(function() {
        if ($(this).html().length > 0) { $(this).removeClass("place_holder"); }
    });
}

function drawChart() {
    $.ajax({
        url : "/admin/dropbox_dash?qs=sizes&tqx=reqId%3A56",
        dataType: "json",
        success: function (data) {
            var ratio = data.quota_used / data.quota_all;
            $("#id_dropbox_sp > div > div.progress-bar-success").css("width", ((1 - ratio) * 100).toString() + '%' ).html(formatSizeUnits(data.quota_avail));
            $("#id_dropbox_sp > div > div.progress-bar-danger").css("width", (ratio * 100).toString() + '%' ).html(formatSizeUnits(data.quota_used));
        }
    });

    $.ajax({
        url : "/admin/dropbox_dash?qs=folders&tqx=reqId%3A57",
        dataType: "json",
        success: function (data) {
            var html = "";
            for (var i = 0; i < data.folders.length; i++) {
                html += '<tr><td><code>' + data.folders[i].name + '</code></td><td><span class="pull-right">' + data.folders[i].shares + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + data.folders[i].nums + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#00f;">' + formatSizeUnits(data.folders[i].sizes) + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="label label-primary">' + data.folders[i].latest + '</span></td></tr>';
            }
            html += '<tr><td colspan="5" style="padding: 0px;"></td></tr>';
            $("#table_dropbox_folder").html(html);
        }
    });


    var chart = new google.visualization.ChartWrapper({
        'chartType': 'AreaChart',
        'dataSourceUrl': '/admin/dropbox_dash?qs=history',
        'containerId': 'plot_dropbpx_files',
        'options': {
            'chartArea': {'width': '90%', 'left': '10%'},
            'legend': {'position': 'none'},
            'title': 'Last 7 Days',
            'titleTextStyle': {'bold': false, 'fontSize': 16},
            'vAxis': {
                'title': '(#)',
                'titleTextStyle': {'bold': true},
            },
            'hAxis': {
                'gridlines': {'count': -1},
                'textStyle': {'italic': true},
                'format': 'MMM dd'
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
}


$(window).on("resize", function() {
    clearTimeout($.data(this, 'resizeTimer'));
    $.data(this, 'resizeTimer', setTimeout(function() {
        for (var i = 0; i < gviz_handles.length; i++) {
            gviz_handles[i].draw();
        }
    }, 200));
});


