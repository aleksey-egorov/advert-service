function updateLotImage(key, id, result) {
    $('#' + key + '_' + id).html(result);
    var Timer=window.setTimeout(function() {
        Upload.initFileUpload(key, id, updatePreloadImage, delPreloadImage);
    },500);
}


function updatePreloadImage(key, id) {
    alert('upd key=' + key);
    alert('id=' + id);
}

function delPreloadImage(key, id) {
    var params = $('#' + key + '_' + id).find(".del_form").serialize();
    $.ajax({
            url: '/user/lot/image/del/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                alert(data);
                //$('#uploaded-file-userphoto-0').val('');
                // Register.updateUserPreloadPhoto();
            }
    });
}


$("#id_brand").autocomplete({
                source: "/autocomplete/brand/",
                minLength: 0,
                mustMatch: true,
                select: function (event, ui) {
                    $('#id_brand').attr("data-id", ui.item.id);
                    //alert($('#brand_id'));
                    //$('#model').autocomplete({source: "/ajax_get/?route=lot/get-models&section=" + $('#section').val() + "&brand=" + $('#brand-id').val()});
                    // $('#model').val('');
                    // $('#model-id').val(0);
                    // $('#model-id').change();
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

$("#delete_button").click(function(e) {
     e.preventDefault();
     //TODO: Lot delete confirmation
});


$("#add_lot_form").submit(function(e) {
     $("#id_brand").val($("#id_brand").attr("data-id"));
     $("#id_product").val($("#id_product").attr("data-id"));
});

$("#add_lot_container select").select2({
        minimumResultsForSearch: Infinity,
        placeholder: "Все"
    });

$("#id_brand").attr('data-id', $("#id_brand_id").val());
$("#id_product").attr('data-id', $("#id_product_id").val());

$("#id_brand_id").val("");
$("#id_product_id").val("");


var Timer=window.setTimeout(function() {
   for(i=1;i<=12;i++) {
        Upload.initFileUpload('userphoto', i, updateLotImage);
   }
},1000);

