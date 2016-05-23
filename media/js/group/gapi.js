var gapi = {
    'gviz_handles': [],
    'fnFormatSize': function(bytes) {
        if      (bytes >= 1000000000) {bytes = (bytes / 1000000000).toFixed(2) + ' GB';}
        else if (bytes >= 1000000)    {bytes = (bytes / 1000000).toFixed(2) + ' MB';}
        else if (bytes >= 1000)       {bytes = (bytes / 1000).toFixed(2) + ' KB';}
        else if (bytes > 1)           {bytes = bytes + ' bytes';}
        else if (bytes == 1)          {bytes = bytes + ' byte';}
        else                          {bytes = '0 byte';}
        return bytes;
    },
    'fnRemovePlaceHolder': function() {
        $(".place_holder").each(function() {
            if ($(this).html().length > 0) { $(this).removeClass("place_holder"); }
        });
    },

    'fnRenderPage': function() {
        if (app.page == 'aws') {
            $.ajax({
                url : "/group/aws_dash/?qs=init&id=init&tp=init&tqx=reqId%3A55",
                dataType: "json",
                success: function (data) {
                    var html = "";
                    for (var i = 0; i < data.table.length; i++) {
                        var ec2 = "", elb = "", ebs = "";
                        if (!data.table[i].hasOwnProperty('ec2')) { data.table[i].ec2 = {'id':'', 'status':-1, 'name':''}; }
                        if (!data.table[i].hasOwnProperty('elb')) { data.table[i].elb = {'id':'', 'status':false, 'name':''}; }
                        if (!data.table[i].hasOwnProperty('ebs')) { data.table[i].ebs = {'id':'', 'status':-1, 'name':''}; }
                        if (data.table[i].ec2.status === 0) {
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
                            if (data.ec2[i].status === 0) {
                                ec2 = '<span class="pull-left"><span class="label label-warning"><span class="glyphicon glyphicon-question-sign"></span></span></span>';
                            } else if (data.ec2[i].status == 16) {
                                ec2 = '<span class="pull-left"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>';
                            } else if (data.ec2[i].status == 48 || data.ec2[i].status == 80) {
                                ec2 = '<span class="pull-left"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';
                            } else if (data.ec2[i].status == 32 || data.ec2[i].status == 64) {
                                ec2 = '<span class="pull-left"><span class="label label-magenta"><span class="glyphicon glyphicon-exclamation-sign"></span></span></span>';
                            }
                            html += '<div class="row" id="ec2-' + data.ec2[i].name + '"><div class="col-lg-9 col-md-9 col-sm-9 col-xs-9"><p><span class="lead">' + ec2 + '&nbsp;&nbsp;<b><u>' + data.ec2[i].name + '</u></b></span>&nbsp;&nbsp;<span class="label label-orange">' + data.ec2[i].id + '</span>&nbsp;<span class="label label-primary">' + data.ec2[i].type + '</span>&nbsp;<span class="label label-info">' + data.ec2[i].arch + '</span>&nbsp;<span class="label label-violet">' + data.ec2[i].region + '</span></p><p><a href="http://' + data.ec2[i].dns + '" target="_blank"><code>' + data.ec2[i].dns + '</code></a></p></div><div class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><p class="text-right"><span class="label label-inverse">Credits Balance</span></p><p class="text-right"><i><mark>' + data.ec2[i].credit + '</mark></i></p></div></div><div class="row"><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div id="plot_cpu_' + data.ec2[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div id="plot_net_' + data.ec2[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div></div>';
                            if (i != data.ec2.length - 1) {
                                html += '<hr/ style="margin: 10px;">';
                            }
                        }
                        $("#aws_ec2_body").html(html).removeClass("place_holder");
                        for (var i = 0; i < data.ec2.length; i++) {
                            gapi.fnDrawEachChart(data.ec2[i].id, '', 'ec2');
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
                            html += '<div class="row" id="elb-' + data.elb[i].name + '"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><p><span class="lead">' + elb + '&nbsp;&nbsp;<b><u>' + data.elb[i].name + '</u></b></span>&nbsp;&nbsp;<span class="label label-orange">' + data.ec2[i].id + '</span>&nbsp;<span class="label label-primary">' + data.ec2[i].type + '</span>&nbsp;<span class="label label-info">' + data.ec2[i].arch + '</span>&nbsp;<span class="label label-violet">' + data.elb[i].region + '</span></p><p><a href="http://' + data.elb[i].dns + '" target="_blank"><code>' + data.elb[i].dns + '</code></a></p></div></div><div class="row"><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div id="plot_lat_' + data.elb[i].name + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div id="plot_req_' + data.elb[i].name + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div></div>';
                            if (i != data.elb.length - 1) {
                                html += '<hr/ style="margin: 10px;">';
                            }
                        }
                        $("#aws_elb_body").html(html).removeClass("place_holder");
                        for (var i = 0; i < data.elb.length; i++) {
                            gapi.fnDrawEachChart(data.elb[i].name, '', 'elb');
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
                            html += '<div class="row" id="ebs-' + data.ebs[i].name + '"><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><p><span class="lead">' + ebs + '&nbsp;&nbsp;<b><u>' + data.ebs[i].name + '</u></b></span>&nbsp;&nbsp;</p><p><span class="label label-orange">' + data.ebs[i].id + '</span>&nbsp;<span class="label label-primary">' + data.ebs[i].type + '</span>&nbsp;<span class="label label-info">' + data.ebs[i].size + ' GB</span>&nbsp;<span class="label label-violet">' + data.ebs[i].region + '</span>' + encrpyed + '</p></div><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div id="plot_disk_' + data.ebs[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div></div>';
                            if (i != data.ebs.length - 1) {
                                html += '<hr/ style="margin: 10px;">';
                            }
                        }
                        $("#aws_ebs_body").html(html).removeClass("place_holder");
                        for (var i = 0; i < data.ebs.length; i++) {
                            gapi.fnDrawEachChart(data.ebs[i].id, '', 'ebs');
                        }
                    }, 1500);
                }
            });

        } else if (app.page == 'ga') {
            $.ajax({
                url : "/group/ga_dash/?qs=init&id=init&tqx=reqId%3A55",
                dataType: "json",
                success: function (data) {
                    var html = "";
                    for (var i = 0; i < data.projs.length; i++) {
                        var ga = (data.projs[i].name.length > 0) ? '<span class="pull-left lead"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></span>' : '<span class="pull-left lead"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></span>';

                        html += '<div class="row"><p><span class="lead">' + ga + '&nbsp;&nbsp;<b><u>' + data.projs[i].name + '</u></b></span>&nbsp;&nbsp;<span class="label label-primary">' + data.projs[i].track_id + '</span><span class="pull-right"><span class="label label-warning">Bounce Rate</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].bounceRate + ' %</span>&nbsp;&nbsp;<span class="label label-orange">Users</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].users + '</span></span></p><p><a href="' + data.projs[i].url + '" target="_blank"><code>' + data.projs[i].url + '</code></a><span class="pull-right"><span class="label label-success">Sessions</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].sessions + '</span>&nbsp;&nbsp;<span class="label label-success">Session Duration</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].sessionDuration + '</span>&nbsp;&nbsp;<span class="label label-info">Page Views</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].pageviews + '</span>&nbsp;&nbsp;<span class="label label-info">Page View / Session</span>&nbsp;<span class="text-right" style="margin-bottom:0px;">' + data.projs[i].pageviewsPerSession + '</span></span></p></div><div class="row"><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div id="chart_session_' + data.projs[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div id="chart_visitor_' + data.projs[i].id + '" class="thumbnail place_holder" style="padding:0px 20px; height: 150px;"></div></div></div>';
                        if (i != data.projs.length - 1) {
                            html += '<hr/ style="margin: 10px;">';
                        }
                    }
                    $("#ga_body").html(html).removeClass("place_holder");
                    for (var i = 0; i < data.projs.length; i++) {
                        gapi.fnDrawEachChart(data.projs[i].id, '', '');
                    }
                }
            });

        } else if (app.page == 'git') {
            $.ajax({
                url : "/group/git_dash/?qs=init&repo=init&org=init&tqx=reqId%3A55",
                dataType: "json",
                success: function (data) {
                    var html = "";
                    for (var i = 0; i < data.git.length; i++) {
                        var lb_private = (data.git[i]['private']) ? '<span class="label label-success">private</span>' : '<span class="label label-magenta">public</span>';

                        html += '<div class="row"><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><p><span class="lead"><mark><b><u>' + data.git[i].org + '/' + data.git[i].name + '</u></b></mark></span>&nbsp;&nbsp;' + lb_private + '</p><p><a href="' + data.git[i].url + '" target="_blank"><code>' + data.git[i].url + '</code></a></p><p id="git-label-' + data.git[i].name + '"></p><table class="table table-hover"><thead><tr class="active"><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Account</th><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-circle-arrow-up"></span>&nbsp;&nbsp;Commits</th><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;Additions</th><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;Deletions</th></tr></thead><tbody>';

                        for (var j = 0; j < data.git[i].data.length; j++) {
                            html += '<tr><td>' + data.git[i].data[j].Contributors + '</td><td><span class="pull-right" style="color:#00f;">' + data.git[i].data[j].Commits + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#080;">' + data.git[i].data[j].Additions + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#f00;">' + data.git[i].data[j].Deletions + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td></tr>';
                        }
                        html += '<tr><td colspan="4" style="padding: 0px;"></td></tr></tbody></table></div><div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div id="plot_c_' + data.git[i].name + '" class="thumbnail git place_holder" style="padding:0px 20px; height: 150px;"></div><div id="plot_ad_' + data.git[i].name + '" class="thumbnail git place_holder" style="padding:0px 20px; height: 150px;"></div></div></div>';
                        if (i != data.git.length - 1) {
                            html += '<hr/ style="margin: 10px;">';
                        }
                    }
                    $("#git_body").html(html).removeClass("place_holder");

                    for (var i = 0; i < data.git.length; i++) {
                        var name = data.git[i].name, org = data.git[i].org;
                        gapi.fnDrawEachChart(name, org, '');
                        $.ajax({
                            url : "/group/git_dash/?qs=num&repo=" + name + "&org=" + org + "&tqx=reqId%3A55",
                            dataType: "json",
                            success: function (data) {
                                $("#git-label-" + data.name.split('/')[1]).html('<span class="label label-green">created</span>&nbsp;<span class="label label-primary">' + data.created_at + '</span>&nbsp;&nbsp;<span class="label label-dark-green">last pushed</span>&nbsp;<span class="label label-primary">' + data.pushed_at + '</span></p><p><span class="label label-danger">issue</span>&nbsp;' + data.num_issues + '&nbsp;&nbsp;<span class="label label-info">download</span>&nbsp;' + data.num_downloads + '&nbsp;&nbsp;<span class="label label-info">pull</span>&nbsp;' + data.num_pulls + '&nbsp;&nbsp;<span class="label label-orange">branch</span>&nbsp;' + data.num_branches + '&nbsp;&nbsp;<span class="label label-orange">fork</span>&nbsp;' + data.num_forks + '&nbsp;&nbsp;<span class="label label-violet">watcher</span>&nbsp;' + data.num_watchers);
                            }
                        });
                    }
                }
            });

        } else if (app.page == 'slack') {
            $.ajax({
                url : "/group/slack_dash/?qs=users&tqx=reqId%3A52",
                dataType: "json",
                success: function (data) {
                    var html = "", presence;
                    for (var i = 0; i < data.owners.length; i++) {
                        presence = (data.owners[i].presence) ? presence = '<span style="color: #50cc32;"': "<span>";
                        html += '<tr><td><span class="pull-right"><span class="label label-danger">' + data.owners[i].id + '</span>&nbsp;&nbsp;' + presence + '<span class="glyphicon glyphicon-registration-mark"></span></span></span></td><td><img src="' + data.owners[i].image + '"/>&nbsp;&nbsp;<i>' + data.owners[i].name + '</i></td></tr>';
                    }
                    for (var i = 0; i < data.admins.length; i++) {
                        presence = (data.admins[i].presence) ? presence = '<span style="color: #50cc32;"': "<span>";
                        html += '<tr><td><span class="pull-right"><span class="label label-success">' + data.admins[i].id + '</span>&nbsp;&nbsp;' + presence + '<span class="glyphicon glyphicon-copyright-mark"></span></span></span></td><td><img src="' + data.admins[i].image + '"/>&nbsp;&nbsp;<i>' + data.admins[i].name + '</i></td></tr>';
                    }
                    for (var i = 0; i < data.users.length; i++) {
                        presence = (data.users[i].presence) ? presence = '<span style="color: #50cc32;"': "<span>";
                        html += '<tr><td><span class="pull-right"><span class="label label-violet">' + data.users[i].id + '</span>&nbsp;&nbsp;' + presence + '<span class="glyphicon glyphicon-ok-circle"></span></span></span></td><td><img src="' + data.users[i].image + '"/>&nbsp;&nbsp;<i>' + data.users[i].name + '</i></td></tr>';
                    }
                    html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
                    for (var i = 0; i < data.gones.length; i++) {
                        presence = (data.gones[i].presence) ? presence = '<span style="color: #50cc32;"': "<span>";
                        html += '<tr class="active"><td><span class="pull-right"><span class="label label-default">' + data.gones[i].id + '</span>&nbsp;&nbsp;' + presence + '<span class="glyphicon glyphicon-ban-circle"></span></span></span></td><td><img src="' + data.gones[i].image + '"/>&nbsp;&nbsp;<i>' + data.gones[i].name + '</i></td></tr>';
                    }            
                    html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
                    $("#table_slack_user").html(html);

                    var ratio = data.gones.length / (data.owners.length + data.admins.length + data.users.length + data.gones.length);
                    $("#id_user_num > div > div.progress-bar-success").css("width", ((1 - ratio) * 100).toString() + '%' ).html(data.owners.length + data.admins.length + data.users.length);
                    $("#id_user_num > div > div.progress-bar-danger").css("width", (ratio * 100).toString() + '%' ).html(data.gones.length);
                }
            });

            $.ajax({
                url : "/group/slack_dash/?qs=channels&tqx=reqId%3A53",
                dataType: "json",
                success: function (data) {
                    var html = "";
                    for (var i = 0; i < data.channels.length; i++) {
                        var name = "", num_msgs = data.channels[i].num_msgs.toString();
                        if (data.channels[i].name == "general" || data.channels[i].name == "random" || data.channels[i].name == "papers" || data.channels[i].name == "calendar") {
                            name = '<span class="label label-info">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-play-circle">';
                        } else if (data.channels[i].name == "dropbox" || data.channels[i].name == "github") {
                            name = '<span class="label label-orange">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-record">';
                        } else {
                            name = '<span class="label label-inverse">' + data.channels[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-ok-circle">';
                        }
                        if (data.channels[i].has_more) { num_msgs = num_msgs + '+'; }
                        html += '<tr><td><span class="pull-right">' + name + '</span></td><td><span class="pull-right">' + data.channels[i].num_members + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + num_msgs + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + data.channels[i].num_files + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="label label-primary">' + data.channels[i].latest + '</span></td></tr>';
                    }
                    html += '<tr><td colspan="2" style="padding: 0px;"></td></tr>';
                    for (var i = 0; i < data.archives.length; i++) {
                        var num_msgs = data.archives[i].num_msgs.toString();
                        // var time = new Date(0);
                        // time.setUTCSeconds(data.archives[i].latest);
                        // latest = time.getFullYear() + '-' + zfill(time.getMonth() + 1, 2) + '-' + zfill(time.getDate(), 2) + ' ' + zfill(time.getHours(), 2) + ':' + zfill(time.getMinutes(), 2) + ':' + zfill(time.getSeconds(), 2);
                        if (data.archives[i].has_more) { num_msgs = num_msgs + '+'; }
                        html += '<tr class="active"><td><span class="pull-right"><span class="label label-default">' + data.archives[i].name + '</span>&nbsp;&nbsp;<span class="glyphicon glyphicon-ban-circle"></span></td><td><span class="pull-right">' + data.archives[i].num_members + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + num_msgs + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + data.archives[i].num_files + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="label label-primary">' + data.archives[i].latest + '</span></td></tr>';
                    }
                    html += '<tr><td colspan="5" style="padding: 0px;"></td></tr>';
                    $("#table_slack_channel").html(html);

                    $("#id_channel_num > div > div.progress-bar-success").css("width", (data.channels.length / (data.archives.length + data.channels.length) * 100).toString() + '%' ).html(data.channels.length);
                    $("#id_channel_num > div > div.progress-bar-danger").css("width", (data.archives.length / (data.archives.length + data.channels.length) * 100).toString() + '%' ).html(data.archives.length);
                }
            });

            $.ajax({
                url : "/group/slack_dash/?qs=files&tqx=reqId%3A54",
                dataType: "json",
                success: function (data) {
                    var html = "";
                    for (var i = 0; i < data.files.types.length; i++) {
                        html += '<tr><td><span class="pull-right"><code>' + data.files.types[i] + '</code></span></td><td><span class="pull-right">' + data.files.nums[i] + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#00f;">' + gapi.fnFormatSize(data.files.sizes[i]) + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td></tr>';
                    }
                    html += '<tr><td colspan="3" style="padding: 0px;"></td></tr>';
                    $("#table_slack_file").html(html);

                    $("#num_file").html('<span class="pull-right">' + data.files.nums[0] + '&nbsp;&nbsp;&nbsp;&nbsp;</span>');
                    $("#size_file").html('<span class="pull-right" style="color:#00f;">' + gapi.fnFormatSize(data.files.sizes[0]) + '&nbsp;&nbsp;&nbsp;&nbsp;</span>');
                }
            });

         
            var chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/group/slack_dash/?qs=plot_msgs',
                'containerId': 'plot_slack_msgs',
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
                    'colors': ['#3ed4e7'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/group/slack_dash/?qs=plot_files',
                'containerId': 'plot_slack_files',
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
                    'colors': ['#ff69bc'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

        } else if (app.page == 'dropbox') {
            $.ajax({
                url : "/group/dropbox_dash/?qs=sizes&tqx=reqId%3A56",
                dataType: "json",
                success: function (data) {
                    var ratio = data.quota_used / data.quota_all;
                    $("#id_dropbox_sp > div > div.progress-bar-success").css("width", ((1 - ratio) * 100).toString() + '%' ).html(gapi.fnFormatSize(data.quota_avail));
                    $("#id_dropbox_sp > div > div.progress-bar-danger").css("width", (ratio * 100).toString() + '%' ).html(gapi.fnFormatSize(data.quota_used));
                }
            });
            $.ajax({
                url : "/group/dropbox_dash/?qs=folders&tqx=reqId%3A57",
                dataType: "json",
                success: function (data) {
                    var html = "";
                    for (var i = 0; i < data.folders.length; i++) {
                        html += '<tr><td><code>' + data.folders[i].name + '</code></td><td><span class="pull-right">' + data.folders[i].shares + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right">' + data.folders[i].nums + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#00f;">' + gapi.fnFormatSize(data.folders[i].sizes) + '&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="label label-primary">' + data.folders[i].latest + '</span></td></tr>';
                    }
                    html += '<tr><td colspan="5" style="padding: 0px;"></td></tr>';
                    $("#table_dropbox_folder").html(html);
                }
            });

            var chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/group/dropbox_dash/?qs=history',
                'containerId': 'plot_dropbox_files',
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
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
        }
    },
    'fnDrawEachChart': function(id, org, type) {
        if (app.page == 'aws') {
            if (type == 'ec2') {
                var chart = new google.visualization.ChartWrapper({
                    'chartType': 'AreaChart',
                    'dataSourceUrl': '/group/aws_dash/?qs=cpu&tp=ec2&id=' + id,
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
                google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
                chart.draw();
                gapi.gviz_handles.push(chart);

                chart = new google.visualization.ChartWrapper({
                    'chartType': 'AreaChart',
                    'dataSourceUrl': '/group/aws_dash/?qs=net&tp=ec2&id=' + id,
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
                google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
                chart.draw();
                gapi.gviz_handles.push(chart);
            } else if (type == 'elb') {
                var chart = new google.visualization.ChartWrapper({
                    'chartType': 'AreaChart',
                    'dataSourceUrl': '/group/aws_dash/?qs=lat&tp=elb&id=' + id,
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
                google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
                chart.draw();
                gapi.gviz_handles.push(chart);

                chart = new google.visualization.ChartWrapper({
                    'chartType': 'AreaChart',
                    'dataSourceUrl': '/group/aws_dash/?qs=req&tp=elb&id=' + id,
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
                google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
                chart.draw();
                gapi.gviz_handles.push(chart);
            } else if (type == 'ebs') {
                var chart = new google.visualization.ChartWrapper({
                    'chartType': 'AreaChart',
                    'dataSourceUrl': '/group/aws_dash/?qs=disk&tp=ebs&id=' + id,
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
                google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
                chart.draw();
                gapi.gviz_handles.push(chart);                
            }

        } else if (app.page == 'ga') {
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
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
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
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

        } else if (app.page == 'git') {
            var chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/group/git_dash/?qs=c&repo=' + id + '&org=' + org,
                'containerId': 'plot_c_' + id,
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Weekly Aggregation',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                        'format': '#',
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM yy'
                    },
                    'tooltip': {'showColorCode': true},
                    'lineWidth': 2,
                    'pointSize': 5,
                    'pointShape': 'square',
                    'colors': ['#3ed4e7'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/group/git_dash/?qs=ad&repo=' + id + '&org=' + org,
                'containerId': 'plot_ad_' + id,
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Weekly Aggregation',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                        'scaleType': 'mirrorLog',
                        'format': 'scientific',
                        'gridlines': {'count': 5}
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM yy'
                    },
                    'tooltip': {'showColorCode': true},
                    'focusTarget': 'category',
                    'lineWidth': 2,
                    'pointSize': 3,
                    'colors': ['#29be92', '#ff5c2b'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
        }
    }
};

var gapi_callback = setTimeout(function() {
    if (google.charts) {
        clearTimeout(gapi_callback);
        gapi.fnRenderPage();
    }
}, 1000);


$(window).on("resize", function() {
    clearTimeout($(window).data(this, 'resizeTimer'));
    $(window).data(this, 'resizeTimer', setTimeout(function() {
        for (var i = 0; i < gapi.gviz_handles.length; i++) {
            gapi.gviz_handles[i].draw();
        }
    }, 200));
});


