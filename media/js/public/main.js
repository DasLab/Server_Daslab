function parse_location() {
  var urls = ['news', 'research', 'people', 'publications', 'resources', 'contact'],
      tab = urls.filter(function(val) { return window.location.pathname.indexOf('/' + val) != -1; });
  if (!tab.length) { return 'home'; }
  return tab[0];
}

function change_view() {
  var tab = parse_location();
  $("a.nav-hover").removeClass().addClass("nav-hover");
  $("#nav-"+ tab).addClass("active");
  $("#main").removeClass().removeAttr("style").addClass("DASmain DAS" + tab);
  if (!$("#DasFOOTER").is(":visible")) {
    $("#DasFOOTER").css("display", "inline");
  }

  if (tab == 'publications') {
    $("table.previous").hide();
    $("p.previous").hide();
    $(".DASpublications").css("height", $("table.current:last").offset().top + 300);

    $("#search").on("click", function() { $("#arrow")[0].click(); });
    $("#arrow2, #expand").on("click", function() {
      $("p.previous").fadeToggle(150);
      $("table.previous").fadeToggle(150, function() {
        if ($(this).is(":visible")) {
          $("#arrow2").children().addClass("imgsp_collapse").removeClass("imgsp_arrow");
          $(".DASpublications").css("height", $("table.previous:last").offset().top + 200);
        } else {
          $("#arrow2").children().removeClass("imgsp_collapse").addClass("imgsp_arrow");
          $(".DASpublications").css("height", $("table.current:last").offset().top + 300);
        }
      });
    });

  } else if (tab == 'people') {
    var current_member = $("tr.current_member").length - 1,
        past_member = $("span.past_member").length,
        height_adjust = current_member * 200 + past_member * 60;
    $(".DASpeople").css("height", height_adjust + 850);

  } else if (tab == 'news') {
    $("tr.previous").hide();
    $(".DASnews").css("height", $("tr.middle").offset().top + 200);

    $("#arrow, #previous").on("click", function() {
      $("tr.previous").fadeToggle(150, function() {
        if ($(this).is(":visible")) {
          $("#arrow").children().addClass("imgsp_collapse").removeClass("imgsp_arrow");
          $(".DASnews").css("height", $("tr.last").offset().top + 200);
        } else {
          $("#arrow").children().removeClass("imgsp_collapse").addClass("imgsp_arrow");
          $(".DASnews").css("height", $("tr.middle").offset().top + 200);
        }
      });
    });

  } else if (tab == 'home' && window.location.pathname == '/') {
    $("#DasFOOTER").css("display", "none");
    $("#home_center").carousel({'interval': 5000, 'keyboard': false, 'pause': 'none'});
  }
}


$(document).ready(function() {
  change_view();

  $("#top").on("click", function (event) {
    event.preventDefault();
    $('#top > div').animate({'right': '-5%', 'opacity': 0}, 125);
    $("html, body").stop().animate({'scrollTop': 0}, 250);
  });

  $("#DasNAV a.nav-hover").on("click", function(event) {
    var href = $(this).attr("href");
    event.preventDefault();

    $("#DasCONTENT").fadeTo(100, 0, function() {
      if (window.history.replaceState) {
        window.history.replaceState({} , '', href);
      } else {
        window.location.href = href;
      }
      $("#DasCONTENT").load(href + " #DasCONTENT", function() {
        change_view();
        $("#DasCONTENT").fadeTo(100, 1);
      });
    });
  });
});


$(window).on("scroll", function() {
  clearTimeout($.data(this, 'resizeTimer'));
  $.data(this, 'resizeTimer', setTimeout(function() {
    if ($(this).scrollTop() > $(window).height() / 2) {
      $('#top > div').animate({'right': '5%', 'opacity': 0.85}, 125);
    } else {
      $('#top > div').animate({'right': '-5%', 'opacity': 0}, 125);
    }
  }, 200));
});