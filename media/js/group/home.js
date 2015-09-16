$.ajax({
    url : "/admin/slack_dash?qs=users&tqx=reqId%3ANone",
    dataType: "json",
    success: function (data) {
		var html = "";
		for (var i = 0; i < data.users.length; i++) {
            var presence = "<span>";
            if (data.users[i].presence) { presence = '<span style="color: #50cc32;"'; }
			html += '<tr><td><span class="pull-right"><span class="label label-violet">' + data.users[i].id + '</span>&nbsp;&nbsp;' + presence + '<span class="glyphicon glyphicon-ok-circle"></span></span></span></td><td><img src="' + data.users[i].image + '"/>&nbsp;&nbsp;<i>' + data.users[i].name + '</i></td></tr>';
		}
		html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
		$("#table_slack_user").html(html);

    }
});


