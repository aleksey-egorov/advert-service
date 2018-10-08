Catalog={
    el: {
        'group' : $('#id_group'),
    },

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
    },
    updateGroupsList: function(category) {
        $.ajax({
             url: '/catalog/groups/list/',
             type: 'get',
             data: 'category=' + category,
             success: function (data, textStatus) {
                 data = data.replace(/&quot;/g, '"');
                 var groups = JSON.parse(data);
                 var gr_options = [{id: -1, text: 'Все'}];
                 groups.forEach(function (item, j, arr) {
                    gr_options.push({id: item.pk, text: item.fields.name});
                 });

                 Catalog.el.group.empty();
                 Catalog.el.group.select2("destroy");
                 Catalog.el.group.select2({
                        data: gr_options,
                        minimumResultsForSearch: Infinity,
                        //templateResult: Catalog.groupOption
                 });
             }
         })
    }
};


$("#filter_wrap button").click(function() {
    $("#filter_wrap button").removeClass('active');
    $(this).addClass('active');
    var val = $(this).attr('data-id');
    $("#filter_form input[name=new_prod_state]").val(val);

    Catalog.activateFilter();
});


$("#filter_wrap select").change(function() {
    Catalog.activateFilter();
});

$("#filter_wrap #id_category").change(function() {
    Catalog.updateGroupsList($(this).val());
});