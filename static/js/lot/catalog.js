Catalog={
    el: {
        'group' : $('#id_group'),
        'brand': $('#id_brand'),
        'region': $('#id_region'),
        'category': $('#id_category'),
        'lots_content' : $("#lots_content"),
        'filter_form': $('#filter_form')
    },
    init: function() {
        Form.initSelect2(Catalog.el.category);
        Form.initSelect2(Catalog.el.group);
        Form.initSelect2(Catalog.el.region);
        Form.initSelect2Ajax(Catalog.el.brand, 'brand');
        Catalog.initPaginator();
    },
    activateFilter:function() {
         var params = Catalog.el.filter_form.serialize();
         console.log("Params: " + params);
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


//#$("#filter_wrap select").select2({
//#        minimumResultsForSearch: Infinity,
//#        placeholder: "Все"
//    });

$("#filter_wrap select").change(function() {
    Catalog.activateFilter();
});

$("#filter_wrap #id_category").change(function() {
    Catalog.updateGroupsList($(this).val());
});

Catalog.init();