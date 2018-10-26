$("#supplier_form").submit(function(e) {
    e.preventDefault();
    var params = $('#supplier_form').serialize();
        $.ajax({
            url: '/sender/supplier_org/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#brand_form').trigger('reset');
                $('#choose_form .result_div').html('Ваше сообщение отправлено!');
            }
        });
});

Geo.initMap();