var weekdayNames = new Array('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');

function label_type(type) {
    if (type == 'GM') {
        return '<span class="label label-primary">Group Meeting</span>';
    } else if (type == 'JC') {
        return '<span class="label label-success">Journal Club</span>';
    } else if (type == 'ES') {
        return '<span class="label label-warning">EteRNA Special</span>';
    } else if (type == 'FS') {
        return '<span class="label label-orange">Flash Slides</span>';
    } else if (type == 'N/A') {
        return '<span class="label label-danger">No Meeting</span>';
    } else {
        return '<span class="label label-default">Unknown</span>';
    }
}


$.ajax({
    url : "/group/dash/schedule/",
    dataType: "json",
    success: function (data) {
        $("#this_type").html(label_type(data['this'].type));
        if (data['this'].type == 'N/A' || data['this'].type == 'FS') {
            $("#this_name").html('(' + data['this'].note + ')').removeClass("label label-inverse").addClass("small");
        } else {
            $("#this_name").html(data['this'].who);
        }
        $("#this_date").html(data['this'].date);
        $("#last_type").html(label_type(data.last.type));
        if (data.last.type == 'N/A'|| data.last.type == 'FS') {
            $("#last_name").html('(' + data.last.note + ')').removeClass("label label-inverse").addClass("small");
        } else {
            $("#last_name").html(data.last.who);
        }
        $("#last_date").html(data.last.date);
        $("#next_type").html(label_type(data.next.type));
        if (data.next.type == 'N/A' || data.next.type == 'FS') {
            $("#next_name").html('(' + data.next.note + ')').removeClass("label label-inverse").addClass("small");
        } else {
            $("#next_name").html(data.next.who);
        }
        $("#next_date").html(data.next.date);
        $("#tp").html('<b>' + weekdayNames[data.weekday] + ' @ ' + data.time.start + ' - ' + data.time.end + ' @ ' + data.place + '</b>');

        $("#recent_flash").html('<span class="label label-primary">' + data.flash_slide.date + '</span>&nbsp;&nbsp;<a href="' + data.flash_slide.url + '" target="_blank"><span class="glyphicon glyphicon-new-window"></span></a>');
        $("#recent_jc").html('<i>' + data.journal_club.name + '</i>&nbsp;&nbsp;<span class="label label-primary">' + data.journal_club.date + '</span>&nbsp;&nbsp;<a href="' + data.journal_club.url + '" target="_blank"><span class="glyphicon glyphicon-new-window"></span></a>');
        $("#recent_eterna").html('<i>' + data.eterna.name + '</i>&nbsp;&nbsp;<span class="label label-primary">' + data.eterna.date + '</span>&nbsp;&nbsp;<a href="' + data.eterna.url + '" target="_blank"><span class="glyphicon glyphicon-new-window"></span></a>');
        $("#recent_rotation").html('<i>' + data.rotation.name + '</i>&nbsp;&nbsp;<span class="label label-primary">' + data.rotation.date + '</span>&nbsp;&nbsp;<a href="/site_data/rot_ppt/' + data.rotation.url + '" target="_blank"><span class="glyphicon glyphicon-new-window"></span></a>');
        $("#recent_archive").html('<i>' + data.archive.name + '</i>&nbsp;&nbsp;<span class="label label-primary">' + data.archive.date + '</span>&nbsp;&nbsp;<a href="/site_data/spe_ppt/' + data.archive.url + '" target="_blank"><span class="glyphicon glyphicon-new-window"></span></a>');
    }
});


$.ajax({
    url : "/group/dash/slack/?qs=home&tqx=reqId%3A50",
    dataType: "json",
    success: function (data) {
        var html = "";
        for (var i = 0; i < data.users.length / 2; i++) {
            var presence1 = '<span class="slack_presence presence_no" data-toggle="tooltip" data-placement="bottom" title="Last Seen: __TS__"><span class="glyphicon glyphicon-unchecked"></span>', presence2 = presence1;
            var u1 = data.users[i], u2 = data.users[i + Math.ceil(data.users.length / 2)];
            if (u1.presence) { presence1 = presence1.replace('presence_no', 'presence_yes').replace('unchecked', 'check'); }
            html += '<tr><td><a target="_blank" href="mailto:' + u1.email + '"><span class="glyphicon glyphicon-envelope"></span></a>&nbsp;&nbsp;' + presence1.replace('__TS__', u1.last_seen) + '</span>&nbsp;&nbsp;<img src="' + u1.image + '"/>&nbsp;&nbsp;<i>' + u1.name + '</i></td>';
            if (typeof u2 === "undefined") {
                html += '<td></td></tr>';
            } else {
                if (u2.presence) { presence2 = presence2.replace('presence_no', 'presence_yes').replace('unchecked', 'check'); }
                html += '<td><a target="_blank" href="mailto:' + u2.email + '"><span class="glyphicon glyphicon-envelope"></span></a>&nbsp;&nbsp;' + presence2.replace('__TS__', u2.last_seen) + '</span>&nbsp;&nbsp;<img src="' + u2.image + '"/>&nbsp;&nbsp;<i>' + u2.name + '</i></td></tr>';
            }
        }
        html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
        $("#table_slack_user").html(html);
        $(".slack_presence").tooltip().hover(function() {
            $("span.glyphicon", this).removeClass("glyphicon-unchecked glyphicon-checked").addClass("glyphicon-log-out");
        }, function() {
            $("span.glyphicon", this).removeClass("glyphicon-log-out").addClass($(this).hasClass("presence_yes") ? "glyphicon-checked" : "glyphicon-unchecked");
        });
    }
});


