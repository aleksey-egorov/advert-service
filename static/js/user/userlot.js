UserLot = {
    updateLotImage: function (key, id, result) {
        $('#' + key + '_' + id).html(result).addClass('changed');
        var Timer = window.setTimeout(function () {
            Upload.initFileUpload(key, id, UserLot.updateLotImage, UserLot.delLotImage);
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
                    Upload.initFileUpload(key, id, UserLot.updateLotImage, UserLot.delLotImage);
                }, 500);
            }
        });
    },

    init: function () {
        var category = $("#id_category");
        var brand = $('#id_brand');
        var product = $('#id_product');

        category.change(function () {
            brand.autocomplete({source: "/acomp/brand/?category=" + category.val()});
            brand.val('').attr("data-id", 0);
            product.val('').attr("data-id", 0);
        });

        brand.autocomplete({
            source: "/acomp/brand/",
            minLength: 0,
            mustMatch: true,
            select: function (event, ui) {
                brand.attr("data-id", ui.item.id);
                product.autocomplete({source: "/acomp/product/?category=" + category.val() + "&brand=" + brand.val()});
                product.val('').attr("data-id", 0);
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

        product.autocomplete({
            source: "/acomp/product/",
            minLength: 0,
            mustMatch: true,
            select: function (event, ui) {
                product.attr("data-id", ui.item.id);
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