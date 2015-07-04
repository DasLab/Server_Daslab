var $ = django.jQuery;

function replace_path(string) {
	return string.replace('/home/ubuntu/Server_DasLab/data/', '/site_data').replace('/MATLAB_Code/Daslab_server/data', '/site_data')
}

$(document).ready(function () {
	// $('script[src="/static/admin/js/admin/DateTimeShortcuts.js"]').remove();
	// $('script[src="/static/admin/js/jquery.js"]').remove();
	// $('script[src="/static/admin/js/jquery.init.js"]').remove();

	$("label.required").css("font-weight", "bold");
	$("table").addClass("table-hover").removeClass("table-bordered table-condensed");
	$('[scope="col"]').addClass("info");

	$("a.deletelink").css("box-sizing", "border-box");
	$("input").addClass("form-control");
	$("select").addClass("form-control");
	$("textarea").addClass("form-control");
	$("span.add-on").html('<span class="glyphicon glyphicon-calendar"></span>').addClass("input-group-addon").removeClass("add-on");

	$('input[type="checkbox"]').each(function() {
		$(this).parent().addClass("checkbox");
		if ($(this).next().is("label")) {
			$(this).prependTo($(this).next());
		} else {
			$(this).parent().removeClass("checkbox");
			$(this).removeClass("form-control");
			$(this).next().css("padding-left", "10px");
		}
	});
	$('p.file-upload>a').each(function() {
		$(this).replaceWith('<div class="form-inline"><label>Current:&nbsp;&nbsp;</label><input class="form-control" disabled="disabled" style="cursor:text;" value="' + $(this).attr("href") + '">&nbsp;&nbsp;<a href="'+ replace_path($(this).attr("href")) + '" class="btn btn-default" target="_blank"><span class="glyphicon glyphicon-cloud-download"></span>&nbsp;&nbsp;View&nbsp;&nbsp;</a></div>');
	});
	$('.clearable-file-input').each(function() {
		$(this).appendTo($(this).prev());
		$(this).children().contents().filter(function () {return this.data === "Clear";}).replaceWith("&nbsp;&nbsp;<span class='glyphicon glyphicon-remove-sign'></span>&nbsp;Clear");
	});
	$('input[type="file"').each(function() {
		$('<div class="form-inline"><label>Change:&nbsp;&nbsp;</label><input id="' + $(this).attr("id") + '_disp" class="form-control" placeholder="No file chosen" disabled="disabled" style="cursor:text;"/>&nbsp;&nbsp;<div id="' + $(this).attr("id") + '_btn" class="fileUpload btn btn-info"><span><span class="glyphicon glyphicon-folder-open"></span>&nbsp;&nbsp;Browse&nbsp;&nbsp;</span></div>').insertAfter(this);
		$(this).detach().appendTo('#' + $(this).attr("id") + '_btn');

        $(this).on("change", function () {
            $('#' + $(this).attr("id") + '_disp').val($(this).val().replace("C:\\fakepath\\", ""));
        });
		$('.file-upload').contents().filter(function () {return this.data === "Change: " | this.data === "Currently: ";}).remove();
	});
	$('input[disabled="disabled"]').each(function() {
		$(this).width($(this).width()*2.5);
	});

	$(".toggle.descending").html('<span class="glyphicon glyphicon-chevron-up"></span>');
	$(".toggle.ascending").html('<span class="glyphicon glyphicon-chevron-down"></span>');
	$(".sortremove").html('<span class="glyphicon glyphicon-remove"></span>');
	$(".sortoptions").addClass("pull-right").removeClass("sortoptions");

    if ($(location).attr("href").indexOf("admin/src/news") != -1) {
		$("th.column-date").addClass("col-md-2");
		$("th.column-content").addClass("col-md-6");
		$("th.column-link").addClass("col-md-4");

		$("td.field-link").css("word-break", "break-all");
		$("td.field-link").css("text-decoration", "underline");

		$("th.column-date>div.text>a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;Date');
		$("th.column-content>div.text>a").html('<span class="glyphicon glyphicon-list-alt"></span>&nbsp;Content');
		$("th.column-link>div.text>a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;URL');

    } else if ($(location).attr("href").indexOf("admin/src/publication") != -1) {
		$("th.column-year").addClass("col-md-1");
		$("th.column-journal").addClass("col-md-2");
		$("th.column-authors").addClass("col-md-3");
		$("th.column-title").addClass("col-md-4");
		$("th.column-link").addClass("col-md-2");

		$("td.field-authors").css("word-break", "break-all");
		$("td.field-title").css("word-break", "break-all");
		$("td.field-link").css("word-break", "break-all");

		$("td.field-journal").css("font-style", "italic");
		$("td.field-title").css("font-weight", "bold");
		$("td.field-link").css("text-decoration", "underline");

		$("th.column-year>div.text>a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;Year');
		$("th.column-journal>div.text>a").html('<span class="glyphicon glyphicon-book"></span>&nbsp;Journal');
		$("th.column-authors>div.text>a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;Authors');
		$("th.column-title>div.text>a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;Title');
		$("th.column-link>div.text>a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;URL');

	} else if ($(location).attr("href").indexOf("admin/src/member") != -1) {
		$("th.column-full_name").addClass("col-md-3");
		$("th.column-year").addClass("col-md-2");
		$("th.column-joint_lab").addClass("col-md-2");
		$("th.column-affiliation").addClass("col-md-5");

		$("th.field-full_name").css("font-weight", "bold");
		$("td.field-year").css("font-style", "italic");

		$("th.column-full_name>div.text>a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;Full Name');
		$("th.column-year>div.text>a").html('<span class="glyphicon glyphicon-hourglass"></span>&nbsp;Status');
		$("th.column-joint_lab>div.text>a").html('<span class="glyphicon glyphicon-home"></span>&nbsp;Joint Lab');
		$("th.column-affiliation>div.text>a").html('<span class="glyphicon glyphicon-education"></span>&nbsp;Affiliation');

	} else if ($(location).attr("href").indexOf("admin/src/flashslide") != -1) {
		$("th.column-date").addClass("col-md-3");
		$("th.column-link").addClass("col-md-9");

		$("td.field-link").css("text-decoration", "underline");

		$("th.column-date>div.text>a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;Date');
		$("th.column-link>div.text>a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;URL');

	} else if ($(location).attr("href").indexOf("admin/src/rotationstudent") != -1) {
		$("th.column-date").addClass("col-md-3");
		$("th.column-full_name").addClass("col-md-3");
		$("th.column-title").addClass("col-md-6");

		$("td.field-full_name").css("font-weight", "bold");

		$("th.column-date>div.text>a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;Date');
		$("th.column-full_name>div.text>a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;Student');
		$("th.column-title>div.text>a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;Title');

 	} else if ($(location).attr("href").indexOf("admin/src/eternayoutube") != -1) {
		$("th.column-date").addClass("col-md-3");
		$("th.column-presenter").addClass("col-md-3");
		$("th.column-title").addClass("col-md-6");
		$("th.column-link").addClass("col-md-6");

		$("td.field-presenter").css("font-weight", "bold");
		$("td.field-link").css("text-decoration", "underline");

		$("th.column-date>div.text>a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;Date');
		$("th.column-presenter>div.text>a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;Presenter');
		$("th.column-title>div.text>a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;Title');
		$("th.column-link>div.text>a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;URL');

 	} else if ($(location).attr("href").indexOf("admin/src/presentation") != -1) {
		$("th.column-date").addClass("col-md-3");
		$("th.column-presenter").addClass("col-md-3");
		$("th.column-title").addClass("col-md-6");

		$("td.field-presenter").css("font-weight", "bold");

		$("th.column-date>div.text>a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;Date');
		$("th.column-presenter>div.text>a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;Student');
		$("th.column-title>div.text>a").html('<span class="glyphicon glyphicon-send"></span>&nbsp;Title');

	} else if ($(location).attr("href").indexOf("admin/auth/user") != -1) {
		$("th.column-username").addClass("col-md-2");
		$("th.column-email").addClass("col-md-3");
		$("th.column-last_login").addClass("col-md-3");
		$("th.column-is_active").addClass("col-md-1");
		$("th.column-is_staff").addClass("col-md-1");
		$("th.column-is_superuser").addClass("col-md-2");

		$("th.field-username").css("font-style", "italic");
		$("td.field-email").css("text-decoration", "underline");

		$("th.column-username>div.text>a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;Username');
		$("th.column-email>div.text>a").html('<span class="glyphicon glyphicon-envelope"></span>&nbsp;Email Address');
		$("th.column-last_login>div.text>a").html('<span class="glyphicon glyphicon-time"></span>&nbsp;Last Login');
		$("th.column-is_active>div.text>a").html('<span class="glyphicon glyphicon-pawn"></span>&nbsp;Active');
		$("th.column-is_staff>div.text>a").html('<span class="glyphicon glyphicon-queen"></span>&nbsp;Staff');
		$("th.column-is_superuser>div.text>a").html('<span class="glyphicon glyphicon-king"></span>&nbsp;Admin');

		$("img[src$='/static/admin/img/icon-yes.gif']").each(function() {
			var newElem = $('<span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span>');
			$(this).replaceWith(newElem);
		});
		$("img[src$='/static/admin/img/icon-no.gif']").each(function() {
			var newElem = $('<span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span>');
			$(this).replaceWith(newElem);
		});
	
	}

});


$(window).load(function () {
	setTimeout(function() {
		if ($(location).attr("href").indexOf("admin/auth/user") == -1) {
			$(".vDateField").each(function () {
				$(this).next().detach().appendTo($(this).parent());
				$(this).removeAttr("size");
				$(this).next().detach().insertAfter($(this).parent());
				$(this).parent().addClass("input-group").removeClass("");
				$('<div class="input-group-btn"><a class="btn btn-default" id="' + $(this).attr("id") + '_cal"><span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Calendar&nbsp;&nbsp;</a></div><div class="input-group-btn"><a class="btn btn-primary" id="' + $(this).attr("id") + '_today"><span class="glyphicon glyphicon-map-marker"></span>&nbsp;&nbsp;Today&nbsp;&nbsp;</a></div>').insertAfter($(this));
				$(this).css("width", "auto");

				if ($(this).parent().next().hasClass("datetimeshortcuts")) {
					var elem = $(this).parent().next();
				} else {
					// $('<br><br>').insertBefore($(this).parent().next());
					$(this).parent().next().css("display", "block")
					var elem = $(this).siblings().last();
				}
				$('#' + $(this).attr("id") + '_cal').attr("href", elem.children().last().attr("href"));
				$('#' + $(this).attr("id") + '_cal').on("click", function() {
					var self = $(this);
					setTimeout(function () {
						$(".calendarbox.module").css("left", self.offset().left);
						$(".calendarbox.module").css("top", self.offset().top + 50);
					}, 50);
				});
				$('#' + $(this).attr("id") + '_today').attr("href", elem.children().first().attr("href"));

				elem.css("display", "none");
			});
		}
	}, 50);

});
