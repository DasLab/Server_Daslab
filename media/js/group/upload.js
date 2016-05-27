$(document).ready(function() {
    $("#form_upload_browse").on("click", function(event) {
        event.preventDefault();
        $("#id_upload_file").trigger("click");
    });
    $("#id_upload_file").on("change", function() {
        $("#form_upload_disp").val($(this).val().replace("C:\\fakepath\\", ""));
    });
    $("#form_upload_today").on("click", function() {
        $("#id_upload_date").val(new Date().toJSON().slice(0, 10));
    });

    $("#form_upload_clear").on("click", function() {
        $("#id_upload_title").val('');
        $("#id_upload_name").val('');
        $("#id_upload_date").val('');
        $("#form_upload_disp").val('');
        $("#id_upload_file").val('');
        $("#id_upload_link").val('');
    });

    $("#form_upload").submit(function(event) {
        event.preventDefault();
        var formData = new FormData($(this)[0]);

        $("#form_upload_msg").parent().addClass("alert-warning").removeClass("alert-danger").removeClass("alert-success");
        $("#form_upload_notice > div > div > p > span").removeClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").addClass("glyphicon-hourglass");
        $("#form_upload_notice > div > div > p > b").html('SENDING');
        $("#form_upload_msg").html('');
        $("#form_upload_notice").fadeIn(250);

        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.messages == 'success') {
                    $("#form_upload_msg").parent().addClass("alert-success").removeClass("alert-warning").removeClass("alert-danger");
                    $("#form_upload_notice > div > div > p > span").addClass("glyphicon-ok-sign").removeClass("glyphicon-remove-sign").removeClass("glyphicon-hourglass");
                    $("#form_upload_notice > div > div > p > b").html('SUCCESS');
                    $("#form_upload_msg").html('File uploaded. Everyone can see it now!');
                    $("#form_upload_clear").trigger("click");
                } else {
                    $("#form_upload_msg").parent().addClass("alert-danger").removeClass("alert-warning").removeClass("alert-success");
                    $("#form_upload_notice > div > div > p > span").addClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").removeClass("glyphicon-hourglass");
                    $("#form_upload_notice > div > div > p > b").html('ERROR');
                    $("#form_upload_msg").html('Incomplete upload fields. Please try again.');
                }
                setTimeout(function() { $("#form_upload_notice").fadeOut(250); }, 2500);
            },
            error: function() {
                $("#form_upload_msg").parent().addClass("alert-danger").removeClass("alert-warning").removeClass("alert-success");
                $("#form_upload_notice > div > div > p > span").addClass("glyphicon-remove-sign").removeClass("glyphicon-ok-sign").removeClass("glyphicon-hourglass");
                $("#form_upload_notice > div > div > p > b").html('ERROR');
                $("#form_upload_msg").html('Internal Server Error.');
             }
        });
    });
});
