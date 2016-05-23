$(document).ready(function() {
     $("#form_email_clear").on("click", function() {
        $("#id_email_from").val('');
        $("#id_email_subject").val('');
        $("#id_email_content").val('');
    });

    $("#form_email").submit(function(event) {
        event.preventDefault();

        $("#form_email_msg").parent().addClass("alert-warning").removeClass("alert-danger").removeClass("alert-success");
        $("#form_email_notice > div > div > p > span").removeClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").addClass("glyphicon-hourglass");
        $("#form_email_notice > div > div > p > b").html('SENDING');
        $("#form_email_msg").html('');
        $("#form_email_notice").fadeIn(250);
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(data) {
                if (data.messages == 'success') {
                    $("#form_email_msg").parent().addClass("alert-success").removeClass("alert-warning").removeClass("alert-danger");
                    $("#form_email_notice > div > div > p > span").addClass("glyphicon-ok-sign").removeClass("glyphicon-remove-sign").removeClass("glyphicon-hourglass");
                    $("#form_email_notice > div > div > p > b").html('SUCCESS');
                    $("#form_email_msg").html('Email sent. The Admin WILL read it!');
                } else {
                    $("#form_email_msg").parent().addClass("alert-danger").removeClass("alert-warning").removeClass("alert-success");
                    $("#form_email_notice > div > div > p > span").addClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").removeClass("glyphicon-hourglass");
                    $("#form_email_notice > div > div > p > b").html('ERROR');
                    $("#form_email_msg").html('Incomplete email fields. Please try again.');
                }
                setTimeout(function() { $("#form_email_notice").fadeOut(250); }, 2500);
            },
            error: function() {
                $("#form_email_msg").parent().addClass("alert-danger").removeClass("alert-warning").removeClass("alert-success");
                $("#form_email_notice > div > div > p > span").addClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").removeClass("glyphicon-hourglass");
                $("#form_email_notice > div > div > p > b").html('ERROR');
                $("#form_email_msg").html('Internal Server Error.');
             }
        });
    });

});

