$("#supplier_form").submit(function(e) {
    e.preventDefault();
    var params = $('#supplier_form').serialize();
        $.ajax({
            url: '/sender/supplier_org/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#supplier_form').trigger('reset');
                $('#contact_form .result_div').html('Ваше сообщение отправлено!');
            }
        });
});

Geo.initMap();