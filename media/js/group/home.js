function label_type(type) {
    if (type == 'GM') {
        return '<span class="label label-primary">Group Meeting</span>'
    } else if (type == 'JC') {
        return '<span class="label label-success">Journal Club</span>'
    } else if (type == 'JC') {
        return '<span class="label label-warning">EteRNA Special</span>'
    } else if (type == 'N/A') {
        return '<span class="label label-danger">No Meeting</span>'
    } else {
        return '<span class="label label-default">Unknown</span>'
    }
}


$.ajax({
    url : "/admin/schedule_dash",
    dataType: "json",
    success: function (data) {
        $("#this_type").html(label_type(data.this[1]));
        if (data.this[1] == 'N/A') {
            $("#this_name").html('(' + data.this[3] + ')').removeClass("label label-inverse").addClass("small");
        } else {
            $("#this_name").html(data.this[2]);
        }
        $("#this_date").html(data.this[0]);
        $("#last_type").html(label_type(data.last[1]));
        if (data.last[1] == 'N/A') {
            $("#last_name").html('(' + data.last[3] + ')').removeClass("label label-inverse").addClass("small");
        } else {
            $("#last_name").html(data.last[2]);
        }
        $("#last_date").html(data.last[0]);
        $("#next_type").html(label_type(data.next[1]));
        if (data.next[1] == 'N/A') {
            $("#next_name").html('(' + data.next[3] + ')').removeClass("label label-inverse").addClass("small");
        } else {
            $("#next_name").html(data.next[2]);
        }
        $("#next_date").html(data.next[0]);
        $("#tp").html('<b>' + data.tp + '</b>');

        $("#recent_flash").html('<span class="label label-primary">' + data.flash_slide.date + '</span>&nbsp;&nbsp;<a href="' + data.flash_slide.url + '" target="_blanl"><span class="glyphicon glyphicon-new-window"></span></a>');
        $("#recent_eterna").html('<span class="label label-primary">' + data.eterna.date + '</span>&nbsp;&nbsp;<a href="' + data.eterna.url + '" target="_blanl"><span class="glyphicon glyphicon-new-window"></span></a><br/><i>' + data.eterna.name + '</i>');
        $("#recent_rotation").html('<span class="label label-primary">' + data.rotation.date + '</span><br/><i>' + data.rotation.name + '</i>');
        $("#recent_archive").html('<span class="label label-primary">' + data.archive.date + '</span><br/><i>' + data.archive.name + '</i>');
    }
});


$.ajax({
    url : "/admin/slack_dash?qs=home&tqx=reqId%3A50",
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


