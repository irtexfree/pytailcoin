const socket = io();
const synth = new Tone.Synth().toDestination();

document.addEventListener("DOMContentLoaded", function () {
  new Vue({
    el: "#chat_vue",
    data: {
      message: "",
      state: "wait_chat",
      chat_id: 0,
      chat: [],
    },
    mounted: function () {
      setInterval(() => {
        socket.emit("stream_pending_support", { user: U_LOGIN });
      }, 100);

      socket.on("stream_chat", (chat) => {
        this.chat = chat["chat"];
        this.chat_id = chat["chat_id"];
        this.state = "chat";
      });

      socket.on("stream_send_message", () => {
        const container = this.$el.querySelector("#chat_container");
        container.scrollTop = container.scrollHeight;
        synth.triggerAttackRelease("C6", "4n");
      });


      socket.on("stream_close_chat", () => {
        this.chat = [];
        this.chat_id = 0;
        this.state = "wait_chat";
      });


      
      socket.on("stream_linked_support", (chat) => {
        if ("user" in chat && "chat_id" in chat["user"]) {
          socket.emit("stream_chat", { chat_id: chat["user"]["chat_id"] });
        }
      });
    },
    methods: {
      send: function () {
        socket.emit("stream_send_message", {
          user: U_LOGIN,
          chat_id: this.chat_id,
          text: this.message,
        });
        this.message = "";
      },
      close_chat: function () {
        socket.emit("stream_close_chat", {
          user: U_LOGIN,
          chat_id: this.chat_id
        });
        this.message = "";
      },
    },
    watch: {
      chat: function (prevent, next) {
        if (prevent.length != next.length) {
          const container = this.$el.querySelector("#chat_container");
          container.scrollTop = container.scrollHeight;
        }
      },
    },
  });


  new Vue({
    el: "#procedure_vue",
    data: {
      search: ""
    },
    computed: {
      filteredList() {
        return this.postList.filter(post => {
          return post.title.toLowerCase().includes(this.search.toLowerCase())
        })
      }
    }
  });
});

 
function urlFormat(value, data = "") {
  return value
    .replace("<activeChatId>", window.x_data_chat.chat_id)
    .replace("<data>", data);
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
    $("#message").prop("disabled", true);

    $.ajax({
      type: method,
      url: urlFormat(url, serialize.get("message")),
      success: function (data) {
        $("#message").val("");
        $("#message").prop("disabled", false);
        $("#chatBox").scrollTop($("#chatBox").height() + 1000);
        $("#message").focus();
      },
    });
  });


  setInterval(() => {
    $.getJSON(urlFormat("/api/ads/3"), function (data) {
      window.x_data_ads = data;
      window.dispatchEvent(new CustomEvent("ads-update", { detail: data }));
    });
  }, 1000);
});
