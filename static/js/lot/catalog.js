Catalog={

    activateFilter:function() {
         var params = $('#filter_form').serialize();
         $.ajax({
             url: '/catalog/lots/list/',
             type: 'post',
             data: params,
             success: function (data, textStatus) {
                 $("#lots_content").html(data);
             }
         })
    }
};


$("#filter_wrap button").click(function() {
    $("#filter_wrap button").removeClass('active');
    $(this).addClass('active');
    var val = $(this).attr('data-id');
    $("#filter_form input[name=prod_state]").val(val);

    Catalog.activateFilter();
});