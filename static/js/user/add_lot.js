UserLot.init();

$("#add_lot_form").submit(function(e) {
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

$("#add_lot_container select").select2({
        minimumResultsForSearch: Infinity,
        placeholder: "Все"
    });

window.setTimeout(function() {
   for(i=0;i<12;i++) {
        Upload.initFileUpload('userphoto', i, UserLot.updateLotImage, UserLot.delLotImage);
   }
}, 500);