Catalog={
    el: {
        'group' : $('#id_group'),
        'lots_content' : $("#lots_content"),
        'filter_form': $('#filter_form')
    },

    activateFilter:function() {
         var params = Catalog.el.filter_form.serialize();
         $.ajax({
             url: '/catalog/lots/list/',
             type: 'post',
             data: params,
             success: function (data, textStatus) {
                 Catalog.el.lots_content.html(data);
                 Catalog.initPaginator();
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
    },
    initPaginator: function() {
        $(".pagination .step-links a").click(function() {
            var val = $(this).attr('data-id');
            Catalog.el.filter_form.find("input[name=page]").val(val);
            Catalog.activateFilter();
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


$("#filter_wrap select").select2({
        minimumResultsForSearch: Infinity,
        placeholder: "Все"
    });


$("#filter_wrap select").change(function() {
    Catalog.activateFilter();
});

$("#filter_wrap #id_category").change(function() {
    Catalog.updateGroupsList($(this).val());
});