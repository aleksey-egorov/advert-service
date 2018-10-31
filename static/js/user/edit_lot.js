UserLot.init();

$("#edit_lot_form").submit(function(e) {
     $("#id_brand").val($("#id_brand").attr("data-id"));
     $("#id_product").val($("#id_product").attr("data-id"));
     var images = [];
     $("#gallery_content .photo_wrap.changed form").each(function() {
         var num = $(this).find('input[name=num]').val();
         var filename = $(this).find('input[name=filename]').val();
         var status = $(this).find('input[name=status]').val();
         images.push({'num': num, 'filename': filename, 'status': status});
     });
     $("#id_image_filenames").val(JSON.stringify(images));
});

$("#edit_lot_container select").select2({
        minimumResultsForSearch: Infinity,
        placeholder: "Все"
    });

// TODO: change to custom widgets
$("#id_brand").attr('data-id', $("#id_brand_id").val());
$("#id_product").attr('data-id', $("#id_product_id").val());
$("#id_brand_id").val("");
$("#id_product_id").val("");



$("#delete_button").click(function(e) {
     e.preventDefault();
     $("#del_reveal").reveal();
     //TODO: Lot delete confirmation
});

$("#del_reveal button.cancel").click(function() {
     $('#del_reveal').trigger('reveal:close');
});
$("#del_reveal button.delete").click(function() {
     var params = $("#del_lot").serialize();
     $.ajax({
            url: '/user/lot/del/',
            type: 'post',
            data: params,
            success: function (data, textStatus) {
                if (data.result == 'deleted') {
                    location.href = '/user/lot/del/done/';
                }
            }
        });
});



window.setTimeout(function() {
   for(i=0;i<12;i++) {
        Upload.initFileUpload('userphoto', i, UserLot.updateLotImage, UserLot.delLotImage);
   }
}, 500);

