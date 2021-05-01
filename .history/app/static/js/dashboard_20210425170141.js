function urlFormat(value, data = "") {
  return value
    .replace("<activeChatId>", window.x_data_chat.chat_id)
    .replace("<data>", data);
}

function x_function_typing(params) {
  $.getJSON("/api/telegram/sendAction/1719949450/typing");  
}

$(function () {

  $(".column").sortable({
    connectWith: ".column",
    handle: ".portlet-header",
    cancel: ".portlet-toggle",
    placeholder:
      "ring-2 ring-indigo-300 bg-indigo-100 transition-all h-28 rounded-xl ui-corner-all p-6 m-6",
  });

  $(".portlet")
    .addClass("ui-widget ui-widget-content ui-helper-clearfix ui-corner-all")
    .find(".portlet-header")
    .addClass("ui-widget-header ui-corner-all")
    .prepend("<span class='ui-icon ui-icon-minusthick portlet-toggle'></span>");

  $(".portlet-toggle").on("click", function () {
    var icon = $(this);
    icon.toggleClass("ui-icon-minusthick ui-icon-plusthick");
    icon.closest(".portlet").find(".portlet-content").toggle();
  });

  $("form#sendMessageForm").submit(function (e) {
    e.preventDefault();

    var form = $(this);
    var url = form.attr("action");
    var method = form.attr("method");
    let serialize = new URLSearchParams(form.serialize());

    $.ajax({
      type: method,
      url: urlFormat(url, serialize.get("message")),
      success: function (data) {},
    });

    // 1719949450/d
  });

  setInterval(() => {
    $.getJSON("/api/telegram/chat/1719949450", function (data) {
      window.x_data_chat = data;
      window.dispatchEvent(new CustomEvent("chat-update", { detail: data }));
    });
  }, 1000);

  setInterval(() => {
    $.getJSON("/api/support/getUserWantHelp", function (data) {
    
      if (data.users) {
        window.x_active_user = data.users[0]['chat_id'];
      } 

      window.x_data_support = data;
      window.dispatchEvent(new CustomEvent("support-update", { detail: data }));
    });
  }, 2000);


});
