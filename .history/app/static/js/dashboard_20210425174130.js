function urlFormat(value, data = "") {
  return value
    .replace("<activeChatId>", window.x_data_chat.chat_id)
    .replace("<data>", data);
}

function x_function_typing() {
  $.getJSON(urlFormat("/api/telegram/sendAction/<activeChatId>/typing"));
}

function x_function_close_current_chat() {
  alert(1)
}

$(function () {
  window.x_data_chat = {
    chat_id: 0,
    chat: [],
  };

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
  });

  setInterval(() => {
    $.getJSON(urlFormat("/api/telegram/chat/<activeChatId>"), function (data) {
      window.x_data_chat = data;
      window.dispatchEvent(new CustomEvent("chat-update", { detail: data }));
    });
  }, 1000);

  setInterval(() => {
    $.getJSON("/api/support/getUserWantHelp", function (data) {
      
      if (data.users) {
        for (item of data.users) {
          if (item.link == '~') {
            $.getJSON(`/api/support/link/${item.chat_id}/${U_LOGIN}`);
            break;
          } else if(item.link == U_LOGIN) {
            window.x_data_chat.chat_id = item.chat_id; 
          }
        } 

      }
    });
  }, 2000);

});
