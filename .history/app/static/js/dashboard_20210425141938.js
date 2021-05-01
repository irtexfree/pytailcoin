function urlFormat(value, data = "") {
  return value
    .replace("<activeChatId>", window.x_data_chat.chat_id)
    .replace("<data>", data);
}
$(function () {
  $(".column").sortable({
    connectWith: ".column",
    handle: ".portlet-header",
    cancel: ".portlet-toggle",
    placeholder:
      "ring-4 ring-indigo-300 bg-indigo-100 transition-all h-28 rounded-xl ui-corner-all",
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

    $.ajax({
      type: method,
      url: url,
      data: form.serialize(),
      success: function (data) {
        alert(data); // show response from the php script.
      },
    });

    // 1719949450/d
  });

  setInterval(() => {
    $.getJSON("/api/telegram/chat/1719949450", function (data) {
      window.x_data_chat = data;
      window.dispatchEvent(new CustomEvent("chat-update", { detail: data }));
    });
  }, 1000);
});
