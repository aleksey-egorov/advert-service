$("#brand_form").submit(function(e) {
    e.preventDefault();
    var params = $('#brand_form').serialize();
        $.ajax({
            url: '/sender/brand/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#brand_form').trigger('reset');
                $('#choose_form .result_div').html('Ваше сообщение отправлено!');
            }
        });
});

Geo.initMap();