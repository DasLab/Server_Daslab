$(document).ready(function () {

	$("a.deletelink").addClass("btn btn-danger");
	$("a.deletelink").css("box-sizing", "border-box");

	$("label.required").css("font-weight", "bold");

	// $("#left-nav>ul>li>ul").css("display", "block");
	// $("#left-nav>ul>li").unbind("mouseover");
	// $("#left-nav>ul>li").off("mouseover");

    if ($(location).attr("href").indexOf("admin/src/news") != -1) {
		$("th.column-date").addClass("span2");
		$("th.column-content").addClass("span6");
		$("th.column-link").addClass("span4");

		$("td.field-link").css("word-break", "break-all");
		$("td.field-link").css("text-decoration", "underline");

    } else if ($(location).attr("href").indexOf("admin/src/publication") != -1) {
		$("th.column-year").addClass("span1");
		$("th.column-journal").addClass("span2");
		$("th.column-authors").addClass("span3");
		$("th.column-title").addClass("span4");
		$("th.column-link").addClass("span2");

		$("td.field-authors").css("word-break", "break-all");
		$("td.field-title").css("word-break", "break-all");
		$("td.field-link").css("word-break", "break-all");

		$("td.field-journal").css("font-style", "italic");
		$("td.field-title").css("font-weight", "bold");
		$("td.field-link").css("text-decoration", "underline");

	} else if ($(location).attr("href").indexOf("admin/src/member") != -1) {
		$("th.column-full_name").addClass("span3");
		$("th.column-year").addClass("span2");
		$("th.column-joint_lab").addClass("span2");
		$("th.column-affiliation").addClass("span5");

		$("th.field-full_name").css("font-weight", "bold");
		$("td.field-year").css("font-style", "italic");

	} else if ($(location).attr("href").indexOf("admin/src/flashslide") != -1) {
		$("th.column-date").addClass("span3");
		$("th.column-link").addClass("span9");

		$("td.field-link").css("text-decoration", "underline");

	} else if ($(location).attr("href").indexOf("admin/src/rotationstudent") != -1) {
		$("th.column-date").addClass("span3");
		$("th.column-full_name").addClass("span3");
		$("th.column-title").addClass("span6");

		$("td.field-full_name").css("font-weight", "bold");

 	} else if ($(location).attr("href").indexOf("admin/src/eternayoutube") != -1) {
		$("th.column-date").addClass("span3");
		$("th.column-presenter").addClass("span3");
		$("th.column-title").addClass("span6");
		$("th.column-link").addClass("span6");

		$("td.field-presenter").css("font-weight", "bold");
		$("td.field-link").css("text-decoration", "underline");

 	} else if ($(location).attr("href").indexOf("admin/src/presentation") != -1) {
		$("th.column-date").addClass("span3");
		$("th.column-presenter").addClass("span3");
		$("th.column-title").addClass("span6");

		$("td.field-presenter").css("font-weight", "bold");

	}


});