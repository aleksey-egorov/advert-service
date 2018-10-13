$("#id_brand").autocomplete({
                source: "/autocomplete/brands/",
                minLength: 0,
                mustMatch: true,
                select: function (event, ui) {
                    $('#brand-id').val(ui.item.id);
                    $('#model').autocomplete({source: "/ajax_get/?route=lot/get-models&section=" + $('#section').val() + "&brand=" + $('#brand-id').val()});
                    $('#model').val('');
                    $('#model-id').val(0);
                    $('#model-id').change();
                },
                response: function (event, ui) {
                    var load = ui.content.length;
                    alert(content);

                    Form.makeCleanField($('#brand'));

                    if (load == 0) {
                        Form.makeError($('#brand'));
                    } else {
                        //Form.makeCorrect($('#' + key + '-region'));
                    }

                    //Form.checkForm(reg,'region');
                }
});