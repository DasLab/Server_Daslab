$(document).ready(function () {

	$("label.required").css("font-weight", "bold");
	$("#left-nav>ul>li>ul").css("display", "block");

	$("a.deletelink").css("box-sizing", "border-box");
	$("input").addClass("form-control");
	$("select").addClass("form-control");

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
			var newElem = $('<span class="label label-success"><span class="glyphicon glyphicon-ok-sign"></span></span>');
			$(this).replaceWith(newElem);
		});
		$("img[src$='/static/admin/img/icon-no.gif']").each(function() {
			var newElem = $('<span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span>');
			$(this).replaceWith(newElem);
		});
	
	}

});