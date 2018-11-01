// Menu
Menu = {
    hide_menu: false,
    timeout: false,
    init: function() {
        var menu_item = $(".menu_a");
        var submenu_item = $('div.submenu');
        var submenu_li = $('div.submenu li');

        menu_item.mouseover(function () {
            Menu.hide_menu = true;
            Menu.hideMenu(menu_item);
            Menu.showMenu($(this));
        });

        menu_item.mouseout(Menu.planMenuHide);

        submenu_item.mouseover(function () {
            Menu.hide_menu = false;
        });

        submenu_li.mouseover(function () {
            Menu.hide_menu = false;
        });

        submenu_item.mouseout(Menu.planMenuHide);
        console.log('menu init');
    },
    showMenu: function(el) {
        el.parent().addClass('active');
    },
    hideMenu: function(el) {
        if (Menu.hide_menu) {
            el.parent().removeClass('active');
        }
    },
    planMenuHide: function() {
        that = this;
        Menu.hide_menu = true;
        Menu.timeout = window.setTimeout(function () {
            Menu.hideMenu($(that));
        }, 200);
    }
};

// Menu
UserMenu = {
    hide_menu: false,
    timeout: false,
    init: function() {
        UserMenu.menu_cont = $("#user_menu");
        var menu_item = $(".usermenu_item");
        var submenu_item = $('div.user_submenu');
        var submenu_li = $('div.user_submenu li');

        menu_item.mouseover(function () {
            UserMenu.hide_menu = true;
            UserMenu.hideMenu();
            UserMenu.showMenu();
            UserMenu.hide_menu = false;
        });

        menu_item.mouseout(UserMenu.planMenuHide);

        UserMenu.menu_cont.mouseover(function () {
            UserMenu.hide_menu = false;
        });

        submenu_li.mouseover(function () {
            UserMenu.hide_menu = false;
        });

        UserMenu.menu_cont.mouseout(UserMenu.planMenuHide);
        console.log('usermenu init');
    },
    showMenu: function(el) {
        UserMenu.menu_cont.addClass('active');
    },
    hideMenu: function(el) {
        if (UserMenu.hide_menu) {
            UserMenu.menu_cont.removeClass('active');
        }
    },
    planMenuHide: function() {
        that = this;
        UserMenu.hide_menu = true;
        UserMenu.timeout = window.setTimeout(function () {
            UserMenu.hideMenu($(that));
        }, 200);
    }
};

// Search
Search = {
    init: function() {
        search_form = $("#main_search_form");
        search_field = $("#main_search");
        search_button = $("#search_button");

        search_form.submit(function(e) {
            e.preventDefault();
            var query=search_field.val();
            var regexp = /tag\:[(\s\w)+]/g;
            if (regexp.test(query)) {
                var words = query.split(":");
                var word = $.trim(words[1]);
                location.href = "/tag/" + word + "/";
            } else {
                location.href = "/search/?q=" + query;
            }
        });

        search_button.click(function() {
            search_form.submit();
        });
    }
};


Upload={
    files:[],
    initFileUpload: function(key, id, add_func, del_func) {

        var file = {};
        file.add_func = add_func;
        file.del_func = del_func;
        file.fileId = id;
        file.key = key;

        $('#'+key+'_'+id+' .upload').fileupload({

            // Функция будет вызвана при помещении файла в очередь
            add: function (e, data) {

                //  var ul = $(this).children('ul');
                var tpl = $('<li><input type="text" value="0" data-width="48" data-height="48"' +
                    ' data-fgColor="#0788a5" data-readOnly="1" data-bgColor="#3e4043" /><p></p><span></span></li>');

                // отслеживание нажатия на иконку отмены
                tpl.find('span').click(function () {
                    if (tpl.hasClass('working')) {
                        jqXHR.abort();
                    }
                    tpl.fadeOut(function () {
                        tpl.remove();
                    });
                });

                // Автоматически загружаем файл при добавлении в очередь
                var jqXHR = data.submit().success(function (result, textStatus, jqXHR) {
                    //var File = '';
                    //alert(result);

                    //if ($('#uploaded-file-'+key+'-'+id)) {
                    //    $('#uploaded-file-'+key+'-'+id).val(File['filename']);
                    //}

                    if (typeof(file.add_func) != 'undefined') {
                        file.add_func(file.key, file.fileId, result);
                    }
                });

            },

            progress: function (e, data) {

                // Вычисление процента загрузки
                var progress = parseInt(data.loaded / data.total * 100, 10);

                // обновляем шкалу
                $(this).find('progress').val(progress).change();

                if (progress == 100) {
                    //data.context.removeClass('working');
                    // UpdatePreview();
                }
            },

            fail: function (e, data) {
                // что-то пошло не так
                data.context.addClass('error');
            }

        });

        Upload.files[file.fileId] = file;
        Upload.initDelButton(file);
        Upload.initAddButton(file);
    },

    initDelButton: function(file) {
        $('#' + file.key + '_' + file.fileId + ' .del .delete').click(function (e) {
            e.preventDefault();
            if (typeof(file.del_func) != 'undefined') {
                file.del_func(file.key, file.fileId);
            }
            Upload.files[file.fileId] = null;
        });
    },

    initAddButton: function(file) {
        $('#' + file.key + '_' + file.fileId + ' .add .addb').click(function (e) {
            if (!$(this).hasClass('disabled')) {
                e.preventDefault();
                $(this).parent().parent().find('input[type=file]').click();
            }
        })
    },

    processUploadResult: function(file) {

    }
};


Geo = {
    initMap: function() {
        var marker = 'dealer';
        var canv = $('#map-canvas');

        var x = canv.attr('data-coord-x');
        var y = canv.attr('data-coord-y');
        var z = parseInt(canv.attr('data-zoom'));

        if (typeof(x) != 'undefined') {
            console.log('marker=' + marker + ' x=' + x + ' y=' + y + ' z=' + z);

            var myLatlng = new google.maps.LatLng(x, y);
            var mapOptions = {
                zoom: z,
                center: myLatlng,
                disableDefaultUI: true,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
            google.maps.event.trigger(map, 'resize');
            map.setZoom(map.getZoom());
            console.log('end map');
        }
    },
    setUserRegion: function(val) {
        $.ajax({
            url: '/acomp/session/',
            type: 'get',
            data: 'region=' + val,
            success: function (data, textStatus) {
                $("#region_selector").html(data.region);
            }
        });
    },
    initRegionSelector: function() {
        var reg_overlay = $('#region_reveal');
        $("#region_selector").click(function() {
             reg_overlay.reveal();
        });

        $.ajax({
             url: '/acomp/region/list/',
             type: 'get',
             success: function (data, textStatus) {
                 var regions = data;
                 var i = 0;
                 var perColumn = Math.ceil(regions.length / 4);

                 regions.forEach(function (item, j, arr) {
                    if (i == 0) {
                        ul = $('<ul class="list"/>')
                    }
                    ul.append('<li><a data-id="' + item.id + '" name="region">' + item.label + '</a></li>');
                    i++;
                    if (i % perColumn == 0) {
                        $('#region_reveal .reveal_inner_inline').append(ul);
                        i = 0;
                    }
                });
                if (i > 0) {
                    $("#region_reveal .reveal_inner_inline").append(ul);
                }
                $('#region_reveal .reveal_inner_inline ul.list a').click(function() {
                    var val=$(this).attr('data-id');
                    Geo.setUserRegion(val);
                    $('#region_reveal').trigger('reveal:close');
                });

             }
        });
    }
};


Form = {
    initSelect2Ajax: function(el, name) {
        $(el).select2({
            placeholder: "Все",
            ajax: {
                url: '/acomp/' + name + '/',
                method: 'get',
                dataType: 'json',
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
                cache: true,
                minimumInputLength: 2
            }
        });
    },
    initSelect2: function(el) {
        $(el).select2({
            minimumResultsForSearch: Infinity,
            placeholder: "Все"
        });
    }
};



