var timeout = '';

// Menu
Menu = {
    hide_menu: false,
    init: function() {
        menu_item = $(".menu_a");
        submenu_item = $('div.submenu');
        submenu_li = $('div.submenu li');

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
        timeout = window.setTimeout(function () {
            Menu.hideMenu($(that));
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


function initMap () {
        var marker='dealer';

        var x=$('#map-canvas').attr('data-coord-x');
        var y=$('#map-canvas').attr('data-coord-y');
        var z=parseInt($('#map-canvas').attr('data-zoom'));

        if (typeof(x)!='undefined') {
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
}
