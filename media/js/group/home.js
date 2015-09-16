$.ajax({
    url : "/admin/slack_dash?qs=users&tqx=reqId%3ANone",
    dataType: "json",
    success: function (data) {
		var html = "";
		for (var i = 0; i < data.users.length / 2; i++) {
            var presence1 = '<span style="color: #808080;"><span class="glyphicon glyphicon-unchecked"></span>', presence2 = presence1;
            var u1 = data.users[i], u2 = data.users[i + Math.round(data.users.length / 2)];
            if (u1.presence) { presence1 = '<span style="color: #50cc32;"><span class="glyphicon glyphicon-check"></span>'; }
            html += '<tr><td><a target="_blank" href="mailto:' + u1.email + '"><span class="glyphicon glyphicon-envelope"></span></a>&nbsp;&nbsp;' + presence1 + '</span>&nbsp;&nbsp;<img src="' + u1.image + '"/>&nbsp;&nbsp;<i>' + u1.name + '</i></td>';
            if (u2 === undefined) {
                html += '<td></td></tr>';
            } else {
                if (u2.presence) { presence2 = '<span style="color: #50cc32;"><span class="glyphicon glyphicon-check"></span>'; }
                html += '<td><a target="_blank" href="mailto:' + u2.email + '"><span class="glyphicon glyphicon-envelope"></span></a>&nbsp;&nbsp;' + presence2 + '</span>&nbsp;&nbsp;<img src="' + u2.image + '"/>&nbsp;&nbsp;<i>' + u2.name + '</i></td></tr>';
            }
		}
		html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
		$("#table_slack_user").html(html);

    }
});


