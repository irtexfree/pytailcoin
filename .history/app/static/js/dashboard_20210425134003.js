$(function () {
    $(".column").sortable({
        connectWith: ".column",
        handle: ".portlet-header",
        cancel: ".portlet-toggle",
        placeholder:
        "ring-4 ring-indigo-300 bg-indigo-100 transition-all h-28 rounded-xl ui-corner-all",
    });

    $(".portlet")
        .addClass(
        "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all"
        )
        .find(".portlet-header")
        .addClass("ui-widget-header ui-corner-all")
        .prepend(
        "<span class='ui-icon ui-icon-minusthick portlet-toggle'></span>"
        );

    $(".portlet-toggle").on("click", function () {
        var icon = $(this);
        icon.toggleClass("ui-icon-minusthick ui-icon-plusthick");
        icon.closest(".portlet").find(".portlet-content").toggle();
    });
    
    $.getJSON('/api/telegram/chat/1719949450', function (data) {
        window.x_data_chat = (data)
        document.querySelector('#chat[x-data]').__x.$data.chat = data.chat
    })
    
});
