// Галерея
$("#unite_gallery").unitegallery({
                gallery_theme: "grid",
                height:500,
                slider_scale_mode: "fit",
                theme_panel_position: "bottom"
});

$("#supplier_form").submit(function(e) {
    e.preventDefault();
    var params = $('#supplier_form').serialize();
        $.ajax({
            url: '/sender/supplier/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#supplier_form').trigger('reset');
                $('#contact_form .result_div').html('Ваше сообщение отправлено!');
            }
        });
});
