google.load('visualization', '1.1', {packages: ['corechart']});
google.setOnLoadCallback(drawDash);

function drawDash() {
	var lineOptions = { 
		'interpolateNulls': true,
		// width: parseInt($("#plot_latency").css("width"))*1.2,
		// left: parseInt($("#plot_latency").css("width"))*0.2,
		legend: { 'position':'bottom' },
		colors: ['#3ed4e7', '#ff912e'],
	};

   	google.visualization.drawChart({
    	chartType: 'LineChart',
    	dataSourceUrl: '/admin/aws_stat?qs=latency',
    	containerId: 'plot_latency',
    	options: lineOptions
    });

	var url = '/admin/aws_stat?qs=23xx';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_23xx');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=45xx';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_45xx');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=request';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_request');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=host';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_host');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=status';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_status');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=network';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_network');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=cpu';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_cpu');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=credit';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_credit');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=volops';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_volops');
    wrapper.draw();

	var url = '/admin/aws_stat?qs=volbytes';
    var wrapper = new google.visualization.ChartWrapper();
    wrapper.setChartType('LineChart');
    wrapper.setDataSourceUrl(url);
    wrapper.setOptions(lineOptions);
    wrapper.setContainerId('plot_volbytes');
    wrapper.draw();

	setTimeout(function() {$(".place_holder").removeClass("place_holder");}, 1000);
}


