const socket = io();
const synth = new Tone.Synth().toDestination();

document.addEventListener("DOMContentLoaded", function () {
  const passport = {
    id: Cookies.get("PASSPORT_ID"),
    secret_key: Cookies.get("PASSPORT_SECRET"),
  };

  window.chat_instance = new Vue({
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
          chat_id: this.chat_id,
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

  window.procedure_instance = new Vue({
    el: "#procedure_vue",
    data: {
      search: "",
      index: 0,
      list: [
        {
          id: 0,
          type: "final-message",
          title: "Закрыть чат (успешный исход)",
          data:
            "Всего доброго, {name}! Было приятно с вами пообщаться. Если у вас появятся еще вопросы, будем рады на них ответить!",
          desc: "Выслать финальное сообщение и закрыть чат",
          tags: ["~"],
        },
        {
          id: 1,
          type: "message",
          title: "Приветственное сообщение",
          data: `Приветствую вас, {name}!\n\nЯ ваш оператор, меня зовут, ${U_LOGIN}\nЧем я могу помочь?`,
          desc: "Выслать приветственное сообщение",
          tags: ["~"],
        },
        {
          id: 2,
          type: "message",
          title: "Как произвести обмен",
          data: "Чтобы произвести обмен ...",
          desc:
            "Выслать сообщение-инструкцию о том, как провести обмен валют через телеграм бота",
          tags: ["~"],
        },
        {
          id: 1001,
          type: "function",
          title: "Добавить кошелек",
          callback: function () {
            wallet_instance.create();
          },
          desc: "Добавить новый кошелек / валюту для обмена",
          tags: ["~"],
        },
      ],
    },
    methods: {
      up: function () {
        if (this.index > 0) {
          this.index = this.index - 1;
        }
      },
      down: function () {
        if (this.index + 1 < this.filteredList.length) {
          this.index = this.index + 1;
        }
      },
      select: function () {
        if (this.filteredList.length > 0) {
          this.procedure(this.filteredList[this.index]["item"]);
        }
      },
      procedure: function (self) {
        this.search = "";
        if (self.type == "message") {
          if (window.chat_instance.state == "chat") {
            socket.emit("stream_send_message", {
              user: U_LOGIN,
              chat_id: window.chat_instance.chat_id,
              text: self.data,
            });
          }
        } else if (self.type == "final-message") {
          if (window.chat_instance.state == "chat") {
            socket.emit("stream_send_message", {
              user: U_LOGIN,
              chat_id: window.chat_instance.chat_id,
              text: self.data,
            });
            socket.emit("stream_close_chat", {
              user: U_LOGIN,
              chat_id: window.chat_instance.chat_id,
            });
          }
        } else if (self.type == "function") {
          self.callback(this);
        }
      },
    },
    computed: {
      filteredList() {
        this.index = 0;

        const options = {
          keys: ["title", "data", "id", "desc", "tags"],
        };

        const fuse = new Fuse(this.list, options);

        return fuse.search(this.search);
      },
    },
  });

  window.modal_instance = new Vue({
    el: "#modal_vue",
    data: {
      show: false,
      title: "Модальное окно",
      fluids: [
        {
          type: "input:text",
          name: "HEllo",
          value: "devel",
          placeholder: "placeholder",
        },
      ],
      submit: () => {},
    },
    methods: {
      create: function (object) {
        this.fluids = object.fluids;
        this.title = object.title;
        this.submit = function () {
          object.submit(
            this,
            _.mapValues(
              _.keyBy($("#modal_data_vue").serializeArray(), "name"),
              "value"
            )
          );
        };
        this.show = true;
      },
      close: function () {
        this.show = false;
      },
    },
  });

  window.wallet_instance = new Vue({
    el: "#wallet_vue",
    data: {
      list: [],
    },
    methods: {
      create: function (object) {
        modal_instance.create({
          title: "Создать кошелек",
          fluids: [
            {
              type: "input:text",
              placeholder: "Название кошелька",
              name: "name",
            },
            { type: "input:text", placeholder: "Адерес", name: "address" },
            { type: "input:number", placeholder: "Объем", name: "value" },
            {
              type: "select:select",
              placeholder: "Валюта",
              name: "currency",
              label: "Валюта",
              value: [
                { value: "BTC", text: "Bitcoin" },
                { value: "RUB_SBER", text: "Русский рубль (Сбербанк)" },
                { value: "RUB_TINK", text: "Русский рубль (Тинькофф)" },
              ],
            },
          ],
          submit: function (self, form) {
            console.log(form);
            socket.emit("stream_create_wallet", {
              form: form,
              passport,
            });
          },
        });
      },
    },
    mounted: function () {
      setInterval(() => {
        socket.emit("stream_wallets", { passport });
      }, 1000);

      socket.on("stream_wallets", (wallets) => {
        this.list = wallets.wallets;
      });
    },
  });
  window.lb_integrate_instance = new Vue({
    el: "#lb_integrate_vue",
    data: {
      list: {
        records: [],
        buys: []
      },
        select: "records",
        screens: [
            { text: "Заявки", value: "records" },
            { text: "Закупки", value: "buys" },
        ]
    },
    mounted: function () {
      setInterval(() => {
        socket.emit("stream_localbitcoins_history", { passport });
      }, 1000);

      socket.on("stream_localbitcoins_history", (history) => {
        this.list.records = history.history;
      });
    },
  });

});

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

});
