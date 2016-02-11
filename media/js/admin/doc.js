$(document).ready(function () {
  $('body').scrollspy({
    'target': '.scroll_nav',
    'offset': 150
  });
  $('.scroll_nav').on('activate.bs.scrollspy', function () {
    $('.scroll_nav > ul > li:not(.active) > ul.panel-collapse').collapse('hide');
    $('.scroll_nav > ul > li.active > ul.panel-collapse').collapse('show');
  });

  $('[id^=tab_]').on('click', function () {
    $('html, body').stop().animate({scrollTop: $($(this).attr("href")).offset().top - 75}, 500);
  });
  $("#top").on("click", function () {
    event.preventDefault();
    $('#top > img').animate({'left':'-5%', 'opacity':'0'}, 125);
    $("html, body").stop().animate({scrollTop: 0}, 250);
  });
  $("#top").hover(
    function(){ $("#top > img").attr("src", "/site_media/images/nav_top.png"); },
    function(){ $("#top > img").attr("src", "/site_media/images/nav_top_hover.png"); }
  );
  
  if ($("#main").width() >= 750) {
    $("#sidebar").css("width", $("#sidebar").width());
    $("#sidebar").affix({
        offset: {
          top: $("#main").position().top
        }
    }); 
  }

  $('ul.panel-collapse').on('show.bs.collapse', function () {
    $(this).parent().find("a>span.glyphicon.pull-right")
      .removeClass("glyphicon-triangle-bottom")
      .addClass("glyphicon-triangle-top");
      
  });
  $('ul.panel-collapse').on('hide.bs.collapse', function () {
    $(this).parent().find("a>span.glyphicon.pull-right")
      .removeClass("glyphicon-triangle-top")
      .addClass("glyphicon-triangle-bottom");
  });

});

$(window).on("scroll", function () {
  clearTimeout($.data(this, 'scrollTimer'));
  $.data(this, 'scrollTimer', setTimeout(function() {
    if ($(this).scrollTop() > $(window).height() / 2) {
      $('#top > img').animate({'left':'0%', 'opacity':'1.0'}, 125);
    } else {
      $('#top > img').animate({'left':'-5%', 'opacity':'0'}, 125);
    }
  }, 200));
});

