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

$("#credit_button").click(function() {
    $("#credit_reveal").reveal();
});

$("#credit_lot").submit(function(e) {
    e.preventDefault();
    var params = $('#credit_lot').serialize();
        $.ajax({
            url: '/sender/credit/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#credit_lot').trigger('reset');
                $('#credit_reveal .result_div').html('Ваше сообщение отправлено!');
            }
        });
});


$("#leasing_button").click(function() {
    $("#leasing_reveal").reveal();
});

$("#leasing_lot").submit(function(e) {
    e.preventDefault();
    var params = $('#leasing_lot').serialize();
        $.ajax({
            url: '/sender/leasing/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#leasing_lot').trigger('reset');
                $('#leasing_reveal .result_div').html('Ваше сообщение отправлено!');
            }
        });
});


$("#rent_button").click(function() {
    $("#rent_reveal").reveal();
});

$("#rent_lot").submit(function(e) {
    e.preventDefault();
    var params = $('#rent_lot').serialize();
        $.ajax({
            url: '/sender/rent/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#rent_lot').trigger('reset');
                $('#rent_reveal .result_div').html('Ваше сообщение отправлено!');
            }
        });
});
