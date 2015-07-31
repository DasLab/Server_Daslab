var $ = django.jQuery;

$(document).ready(function () {
	$("#left-nav>ul>li>ul").css("display", "block");

	$(".left-nav>ul").addClass("nav nav-pills nav-stacked");
	$(".left-nav>ul>li.active>a").css("background-color", "#5496d7");
	$(".left-nav>ul>li.active>a").css("font-size", 20);
	$(".left-nav>ul>li>ul>li.active>a").css("color", "#fff");
	$(".left-nav>ul>li>ul>li.active>a").css("background-color", "#ff912e");

	$('i[class^="icon"]').each(function() {
		$(this).replaceWith('<span class="glyphicon glyph' + $(this).attr("class") + '"></span>&nbsp;&nbsp;');
	});
	$(".form-search>span.glyphicon").remove();
	$(".form-search>input.submit").attr("id", "search_submit");
	$("#search_submit").replaceWith("<button type='submit' class='submit form-control' id='search_submit' style='border:none;'><span class='glyphicon glyphicon-search'></span>&nbsp;</button>");


	$('.left-nav>ul>li>ul>li>a[href="/admin/apache/"]').html('<span class="glyphicon glyphicon-grain"></span>&nbsp;&nbsp;Apache Status');
	$('.left-nav>ul>li>ul>li>a[href="/admin/aws/"]').html('<span class="glyphicon glyphicon-text-background"></span>&nbsp;&nbsp;AWS Console');
	$('.left-nav>ul>li>ul>li>a[href="/admin/ga/"]').html('<span class="glyphicon glyphicon-signal"></span>&nbsp;&nbsp;Google Analytics');
	$('.left-nav>ul>li>ul>li>a[href="/admin/git/"]').html('<span class="glyphicon glyphicon-compressed"></span>&nbsp;&nbsp;Github Repository');
	$('.left-nav>ul>li>ul>li>a[href="/admin/dir/"]').html('<span class="glyphicon glyphicon-folder-open"></span>&nbsp;&nbsp;Directory');
	$('.left-nav>ul>li>ul>li>a[href="/admin/backup/"]').html('<span class="glyphicon glyphicon-floppy-open"></span>&nbsp;&nbsp;Backup Schedule');

	$('.left-nav>ul>li>ul>li>a[href="/admin/src/news/"]').html('<span class="glyphicon glyphicon-picture"></span>&nbsp;&nbsp;News Items');
	$('.left-nav>ul>li>ul>li>a[href="/admin/src/member/"]').html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Member Management');
	$('.left-nav>ul>li>ul>li>a[href="/admin/src/publication/"]').html('<span class="glyphicon glyphicon-education"></span>&nbsp;&nbsp;Publication Entries');
	$('.left-nav>ul>li>ul>li>a[href="/admin/export/"]').html('<span class="glyphicon glyphicon-floppy-save"></span>&nbsp;&nbsp;Publication Export');

	$('.left-nav>ul>li>ul>li>a[href="/admin/auth/user/"]').html('<span class="glyphicon glyphicon-lock"></span>&nbsp;&nbsp;User Autherization');
	$('.left-nav>ul>li>ul>li>a[href="/admin/src/flashslide/"]').html('<span class="glyphicon glyphicon-blackboard"></span>&nbsp;&nbsp;Flash Slides');
	$('.left-nav>ul>li>ul>li>a[href="/admin/src/eternayoutube/"]').html('<span class="glyphicon glyphicon-facetime-video"></span>&nbsp;&nbsp;EteRNA Open Group Meetings');
	$('.left-nav>ul>li>ul>li>a[href="/admin/src/rotationstudent/"]').html('<span class="glyphicon glyphicon-retweet"></span>&nbsp;&nbsp;Rotation Students');
	$('.left-nav>ul>li>ul>li>a[href="/admin/src/presentation/"]').html('<span class="glyphicon glyphicon-cd"></span>&nbsp;&nbsp;Archived Presentations');


	$('.left-nav>ul>li>ul>li>a[href="/admin/aws/"]').attr("disabled", "disabled").css("text-decoration", "line-through").attr("href", "");

});
