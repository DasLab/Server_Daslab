function sign(x){return x>0?1:x<0?-1:x;}

function change_view(href) {
  $("a.nav-hover").removeClass().addClass("nav-hover");
  $("#main").removeClass().addClass("DASmain");

  if (href.indexOf('/contact') != -1) {
    $("#main").addClass("DAScontact");
    $("#nav-contact").addClass("active");
    $("#DasFOOTER").css({"top": "1013px", "display": "inline"});
    $("#DasICON").css({"top": "1068px", "display": "inline"});

  } else if (href.indexOf('/resources') != -1) {
    $("#main").addClass("DASresources");
    $("#nav-resources").addClass("active");
    $("#DasFOOTER").css({"top": "1500px", "display": "inline"});
    $("#DasICON").css({"top": "1555px", "display": "inline"});

  } else if (href.indexOf('/publications') != -1) {
    $("#main").addClass("DASpub");
    $("#nav-publications").addClass("active");
    $("table.previous").hide();
    $("p.previous").hide();

    $("#DasFOOTER").css({"top": $("table.current:last").offset().top + 200, "display": "inline"});
    $("#DasICON").css({"top": parseInt($("#DasFOOTER").css("top")) + 55, "display": "inline"});
    $(".DASpub").css("height", parseInt($("#DasFOOTER").css("top")) + 150);

    $("#search").on("click", function () { $("#arrow")[0].click(); });
    $("#arrow2, #expand").on("click", function () {
      $("table.previous").toggle();
      $("p.previous").toggle();
      var flag = sign(($("table.previous").css("display") == "none") - 0.5);

      if (flag == -1) {
        $("#arrow2").children().addClass("imgsp_collapse").removeClass("imgsp_arrow");
        $("#DasFOOTER").css("top", $("table.previous:last").offset().top + 200);
      } else {
        $("#arrow2").children().removeClass("imgsp_collapse").addClass("imgsp_arrow");
        $("#DasFOOTER").css("top", $("table.current:last").offset().top + 200);
      }
      $("#DasICON").css("top", parseInt($("#DasFOOTER").css("top")) + 55);
      $(".DASpub").css("height", parseInt($("#DasFOOTER").css("top")) + 150);
    });

  } else if (href.indexOf('/people') != -1) {
    $("#main").addClass("DASpeople");
    $("#nav-people").addClass("active");

    var current_member = $("tr.current_member").length - 1,
        past_member = $("span.past_member").length,
        height_adjust = current_member * 200 + past_member * 60;
    $("#DasFOOTER").css({"top": 750 + height_adjust, "display": "inline"});
    $("#DasICON").css({"top": parseInt($("#DasFOOTER").css("top")) + 55, "display": "inline"});
    $(".DASpeople").css("height", parseInt($("#DasFOOTER").css("top")) + 150);

  } else if (href.indexOf('/news') != -1) {
    $("#main").addClass("DASnews");
    $("#nav-news").addClass("active");
    $("tr.previous").hide();

    $("#DasFOOTER").css({"top": $("tr.middle").offset().top + 50, "display": "inline"});
    $("#DasICON").css({"top": parseInt($("#DasFOOTER").css("top")) + 55, "display": "inline"});
    $(".DASnews").css("height", parseInt($("#DasFOOTER").css("top")) + 150);

    $("#arrow, #previous").on("click", function () {
      $("tr.previous").toggle();
      var flag = sign(($("tr.previous").css("display") == "none") - 0.5);

      if (flag == -1) {
        $("#arrow").children().addClass("imgsp_collapse").removeClass("imgsp_arrow");
        $("#DasFOOTER").css("top", $("tr.last").offset().top + 50);
      } else {
        $("#arrow").children().removeClass("imgsp_collapse").addClass("imgsp_arrow");
        $("#DasFOOTER").css("top", $("tr.middle").offset().top + 50);
      }
      $("#DasICON").css("top", parseInt($("#DasFOOTER").css("top")) + 55);
      $(".DASnews").css("height", parseInt($("#DasFOOTER").css("top")) + 150);
    });

  } else if (href.indexOf('/research') != -1) {
    $("#main").addClass("DASresearch");
    $("#nav-research").addClass("active");
    $("#DasFOOTER").css({"top": "1346px", "display": "inline"});
    $("#DasICON").css({"top": "1401px", "display": "inline"});

  } else {
    console.log(href)
    $("#main").addClass("DAShome");
    $("#nav-home").addClass("active");
    $("#DasICON").css({"top": "673px", "display": "inline"});
    $("#DasFOOTER").css("display", "none");

    $("#home_center").carousel({'interval': 5000, 'keyboard': false, 'pause': 'none'});
  }

}


$(document).ready(function () {
  change_view(window.location.href);

  $("#top").on("click", function (event) {
    event.preventDefault();
    $('#top > div').animate({'right': '-5%', 'opacity': 0}, 125);
    $("html, body").stop().animate({'scrollTop': 0}, 250);
  });

  $("#DasNAV a.nav-hover").on("click", function(event) {
    event.preventDefault();
    $("#DasCONTENT").fadeOut(150);
    if (window.history.replaceState) {
      window.history.replaceState({} , '', $(this).attr("href"));
    } else {
      window.location.hrefhref = $(this).attr("href");
    }
    $("#DasCONTENT").load($(this).attr("href") + " #DasCONTENT", function() {
      change_view(window.location.href);
      $("#DasCONTENT").fadeIn(100);
    });
  });
});


$(window).on("scroll", function () {
  clearTimeout($.data(this, 'resizeTimer'));
  $.data(this, 'resizeTimer', setTimeout(function() {
    if ($(this).scrollTop() > $(window).height() / 2) {
      $('#top > div').animate({'right': '5%', 'opacity': 0.85}, 125);
    } else {
      $('#top > div').animate({'right': '-5%', 'opacity': 0}, 125);
    }
  }, 200));
});