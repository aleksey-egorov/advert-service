UserLot = {
    updateLotImage: function (key, id, result) {
        $('#' + key + '_' + id).html(result).addClass('changed');
        var Timer = window.setTimeout(function () {
            Upload.initFileUpload(key, id, updateLotImage, delLotImage);
        }, 500);
    },

    delLotImage: function (key, id) {
        var params = $('#' + key + '_' + id).find(".del_form").serialize();
        $.ajax({
            url: '/user/lot/image/del/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                $('#' + key + '_' + id).html(data).addClass('changed');
                var Timer = window.setTimeout(function () {
                    Upload.initFileUpload(key, id, updateLotImage, delLotImage);
                }, 500);
            }
        });
    },

    init: function () {

        $("#id_category").change(function () {
            $('#id_brand').autocomplete({source: "/autocomplete/brand/?category=" + $('#id_category').val()});
        });

        $("#id_brand").autocomplete({
            source: "/autocomplete/brand/",
            minLength: 0,
            mustMatch: true,
            select: function (event, ui) {
                $('#id_brand').attr("data-id", ui.item.id);
                $('#id_product').autocomplete({source: "/autocomplete/brand/?category=" + $('#id_category').val()});
                $('#id_product').val('').attr("data-id", 0);
            },
            response: function (event, ui) {
                var load = ui.content.length;

                //Form.makeCleanField($('#brand'));
                if (load == 0) {
                    //Form.makeError($('#brand'));
                } else {
                    //Form.makeCorrect($('#' + key + '-region'));
                }
                //Form.checkForm(reg,'region');
            }
        });

        $("#id_product").autocomplete({
            source: "/autocomplete/product/",
            minLength: 0,
            mustMatch: true,
            select: function (event, ui) {
                $('#id_product').attr("data-id", ui.item.id);

                //$('#model').autocomplete({source: "/ajax_get/?route=lot/get-models&section=" + $('#section').val() + "&brand=" + $('#brand-id').val()});
                //$('#model').val('');
                //$('#model-id').val(0);
                //$('#model-id').change();
            },
            response: function (event, ui) {
                var load = ui.content.length;

                //Form.makeCleanField($('#brand'));

                if (load == 0) {
                    //Form.makeError($('#brand'));
                } else {
                    //Form.makeCorrect($('#' + key + '-region'));
                }

                //Form.checkForm(reg,'region');
            }
        });

    }
};