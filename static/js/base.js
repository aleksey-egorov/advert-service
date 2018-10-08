
var timeout = '';
var hide_menu = false;
var menu_item = $(".menu_a");
var submenu_item = $('div.submenu');
var submenu_li = $('div.submenu li');

// Menu
menu_item.mouseover(function() {
    hide_menu = true;
    hideMenu(menu_item);
    showMenu($(this));
    //activateMenu($(this));
});

menu_item.mouseout(planMenuHide);

submenu_item.mouseover(function() {
     hide_menu = false;
});

submenu_li.mouseover(function() {
     hide_menu = false;
});

submenu_item.mouseout(planMenuHide);



function showMenu(el) {
    el.parent().addClass('active');
}

function hideMenu(el) {
    if (hide_menu) {
        el.parent().removeClass('active');
    }
}


function planMenuHide() {
    that=this;
    hide_menu = true;
    timeout = window.setTimeout(function() {
                    hideMenu($(that));
           },200);
}

//

$("select.select2").select2({
        minimumResultsForSearch: Infinity,
        placeholder: "Все"
    });