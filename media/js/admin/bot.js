$(document).ready(function() {
    $("#id_day_meeting").prop("disabled", true);

    $("#id_is_slack").on("change", function() {
        if ($(this).is(":checked")) {
            $("#id_is_bday").prop("disabled", false);
            $("input[id^='id_is_admin'").prop("disabled", false);
            $("input[id^='id_is_duty'").prop("disabled", false);
            $("input[id^='id_is_user'").prop("disabled", false);
            $("select[id^='id_day_duty'").prop("disabled", false);

            if (!$("#id_is_version").is(":checked")) {
                $("#id_is_admin_version").prop("disabled", true);
            }
            if (!$("#id_is_report").is(":checked")) {
                $("#id_is_admin_report").prop("disabled", true);
            }
            if (!$("#id_is_bday").is(":checked")) {
                $("#id_is_duty_bday").prop("disabled", true);
            }
            $("select[id^='id_day_reminder']").prop("disabled", false);
        } else {
            $("#id_is_bday").prop("disabled", true);
            $("input[id^='id_is_admin'").prop("disabled", true);
            $("input[id^='id_is_duty'").prop("disabled", true);
            $("input[id^='id_is_user'").prop("disabled", true);
            $("select[id^='id_day_duty'").prop("disabled", true);

            if (!$("#id_is_flash_slide").is(":checked")) {
                $("select[id^='id_day_reminder']").prop("disabled", true);
            } else {
                $("select[id^='id_day_reminder']").prop("disabled", false);
            }
        }
    });

    $("#id_is_cache").on("change", function() {
        if ($(this).is(":checked")) {
            $("select[id^='id_cache'").prop("disabled", false);
        } else {
            $("select[id^='id_cache'").prop("disabled", true);
        }
    });

    $("#id_is_version").on("change", function() {
        if ($(this).is(":checked")) {
            if ($("#id_is_slack").is(":checked")) {
                $("#id_is_admin_version").prop("disabled", false);
            }
        } else {
            $("#id_is_admin_version").prop("disabled", true);
        }
    });
    $("#id_is_report").on("change", function() {
        if ($(this).is(":checked")) {
            if ($("#id_is_slack").is(":checked")) {
                $("#id_is_admin_report").prop("disabled", false);
            }
        } else {
            $("#id_is_admin_report").prop("disabled", true);
        }
    });

    $("#id_is_bday").on("change", function() {
        if ($(this).is(":checked")) {
            if ($("#id_is_slack").is(":checked")) {
                $("#id_is_duty_bday").prop("disabled", false);
            }
        } else {
            $("#id_is_duty_bday").prop("disabled", true);
        }
    });

    $("#id_is_flash_slide").on("change", function() {
        if ($(this).is(":checked") || $("#id_is_slack").is(":checked")) {
            $("select[id^='id_day_reminder']").prop("disabled", false);
        } else {
            $("select[id^='id_day_reminder']").prop("disabled", true);
        }
    });

    // $("#id_order_number").on("change", function() {
    //  $(".item_num").toggle();
    //  $("[id^=id_number_order]").trigger("change");
    // });
    // $("[id^=id_number_order]").trigger("change");

    // $(".item_das").css("font-weight", "bold");
    // $("#id_bold_author").on("change", function() {
    //  if ($("#id_bold_author").is(":checked")) {
    //      $(".item_das").css("font-weight", "bold");
    //  } else {
    //      $(".item_das").css("font-weight", "normal");
    //  }
    // });
});


