$(document).ready(function () {
    $("#form_upload_browse").on("click", function(event) {
        event.preventDefault();
        $("#id_upload_file").trigger("click");
    });
    $("#id_upload_file").on("change", function () {
        $("#form_upload_disp").val($(this).val().replace("C:\\fakepath\\", ""));
    });
    $("#form_upload_today").on("click", function () {
        $("#id_upload_date").val(new Date().toJSON().slice(0,10));
    });

    $("#form_upload_clear").on("click", function() {
        $("#id_upload_title").val('');
        $("#id_upload_name").val('');
        $("#id_upload_date").val('');
        $("#form_upload_disp").val('');
        $("#id_upload_file").val('');
        $("#id_upload_link").val('');
    });

});
