// Галерея
$("#unite_gallery").unitegallery({
                gallery_theme: "grid",
                height:500,
                slider_scale_mode: "fit",
                theme_panel_position: "bottom"
});

$("#brand_form").submit(function(e) {
    e.preventDefault();
    var params = $('#brand_form').serialize();
        $.ajax({
            url: '/sender/brand/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#brand_form').trigger('reset');
                $('#contact_form .result_div').html('Ваше сообщение отправлено!');
            }
        });
});
