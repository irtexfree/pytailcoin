const socket = io();
const audio = {
  new_chat: new Audio('/ogg/consequence-544.ogg'),
  send_message: new Audio('/ogg/pull-out-551.ogg'),
  new_notification: new Audio('/ogg/beyond-doubt-2-581.ogg'),
  close_chat: new Audio('/ogg/your-turn-491.ogg'),
}

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
                socket.emit("stream_pending_support", {user: U_LOGIN});
            }, 1000);

            socket.on("stream_chat", (chat) => {
                this.chat = chat["chat"];
                this.chat_id = chat["chat_id"];
                this.state = "chat";
            });

            socket.on("stream_send_message", () => {
                const container = this.$el.querySelector("#chat_container");
                container.scrollTop = container.scrollHeight;
            });

            socket.on("stream_close_chat", () => {
                this.chat = [];
                this.chat_id = 0;
                this.state = "wait_chat";
                audio.close_chat.play()
            });

            socket.on("stream_linked_support", (chat) => {
                if (this.chat_id == 0) {
                    if ("user" in chat && "chat_id" in chat["user"]) {
                        socket.emit("stream_chat", {chat_id: chat["user"]["chat_id"]});
                        audio.new_chat.play()
                    }
                } else {
                    socket.emit("stream_chat", {chat_id: chat["user"]["chat_id"]});
                }

            });
        },
        methods: {
            send: function () {
                if (this.message != "") {
                    socket.emit("stream_send_message", {
                        user: U_LOGIN,
                        chat_id: this.chat_id,
                        text: this.message,
                    });
                    this.message = "";
                    audio.send_message.play()
                }
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
                if (prevent.length !== next.length) {
                    const container = this.$el.querySelector("#chat_container");
                    if (container && 'scrollHeight' in container) {
                        container.scrollTop = container.scrollHeight;
                    }
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
                        "Всего доброго! Было приятно с вами пообщаться. Если у вас появятся еще вопросы, будем рады на них ответить!",
                    desc: "Выслать финальное сообщение и закрыть чат",
                    tags: ["~"],
                },
                {
                    id: 1,
                    type: "message",
                    title: "Приветственное сообщение",
                    data: `Я ваш оператор, меня зовут, ${Cookies.get("first_name")}\nЧем я могу помочь?`,
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
                {
                    id: 9001,
                    type: "function",
                    title: "Авторизоваться на Localbitcoins",
                    callback: function () {
                        lb_integrate_instance.auth();
                    },
                    desc: "Войти в аккаунт Localbitcoins",
                    tags: ["~"],
                },
                {
                    id: 9002,
                    type: "function",
                    title: "Авторизоваться на Binance",
                    callback: function () {
                        binance_integrate_instance.auth();
                    },
                    desc: "Войти в аккаунт Binance",
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
            fluids: [],
            submit: () => {
            },
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
            create: function () {
                modal_instance.create({
                    title: "Создать кошелек",
                    fluids: [
                        {
                            type: "input:text",
                            placeholder: "Название кошелька",
                            name: "name",
                        },
                        {type: "input:text", placeholder: "Адрес", name: "address"},
                        {type: "input:number", placeholder: "Объем", name: "value"},
                        {
                            type: "select:select",
                            placeholder: "Валюта",
                            name: "currency",
                            label: "Валюта",
                            value: [
                                {value: "BTC", text: "Bitcoin"},
                                {value: "RUB_SBER", text: "Русский рубль (Сбербанк)"},
                                {value: "RUB_TINK", text: "Русский рубль (Тинькофф)"},
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
                socket.emit("stream_wallets", {passport});
            }, 1000);

            socket.on("stream_wallets", (wallets) => {
                this.list = wallets.wallets;
            });
        },
    });

    window.lb_integrate_instance = new Vue({
        el: "#lb_integrate_vue",
        data: {
            chat_id: 0,
            list: {
                records: [],
                buys: []
            },
            select: "records",
            subselect: null,
            screens: [
                {text: "Заявки", value: "records"},
                {text: "Закупки", value: "buys"},
                {text: "Настройки", value: "settings"}
            ],
            payment_methods: {},
            form: {
                buy: {payment_methods: {}},
                notify: {payment_methods: {}}
            }
        },
        methods: {
            auth: function () {
                modal_instance.create({
                    title: "Авторизация в Localbitcoins.net",
                    fluids: [
                        {
                            type: "input:text",
                            placeholder: "HAPI ключ",
                            name: "hapikey",
                        },
                        {
                            type: "input:text",
                            placeholder: "HAPI секрет",
                            name: "hapisecret",
                        },
                    ],
                    submit: function (self, form) {
                        socket.emit("stream_integrate_lb_auth", {
                            form: form,
                            passport,
                        });
                    },
                });
            },
            currency: function (x) {
                return (new Intl.NumberFormat('ru-RU').format(x)) + " руб"
            },
            amount: function (x) {
                return (new Intl.NumberFormat('ru-RU').format(x))
            },
            submit: function() {
                socket.emit("stream_localbitcoins_update_props", {
                    passport,
                    form: this.form
                });
            },
            get_chat: function (contact_id) {
                socket.emit("stream_lb_chat", { passport, form: { contact_id } })
            },
            send: function (contact_id, msg) {
                socket.emit("stream_lb_chat_send", { passport, form: { contact_id, msg } })
            },
            cancel_order: function (contact_id) {
                socket.emit("stream_lb_cancel_order", { passport, form: { contact_id } })
            },
        },
        mounted: function () {
            setInterval(() => {
                socket.emit("stream_localbitcoins_history", {passport});
                socket.emit("stream_localbitcoins_orders", {passport});
            }, 1000);

            socket.on("stream_localbitcoins_history", (history) => {
                this.list.records = history.history;
            });

            socket.on("stream_localbitcoins_orders", (orders) => {
this.list.buys = orders.orders;
            });


            socket.on("stream_payment_methods", (data) => {
                this.payment_methods = data.methods
            })

            socket.on("stream_localbitcoins_update_props", (data) => {
                this.form = data;
            })

            socket.on("stream_lb_chat", (data) => {
                this.lb_chat_id = data.contact_id;
                modal_instance.create({
                    title: "Быстрый чат (Альфа версия)",
                    fluids: _.concat(_.map(data.chat_history, e => {
                      return {
                            type: "chat:chat",
                            value: e.msg,
                            name: e.sender.name,
                        }
                    }), [
                        {
                            type: "input:text",
                            name: "message",
                            placeholder: "Наберите сообщение и нажмите 'Сохранить', чтобы отправить сообщение"
                        }
                    ]),
                    submit: function (self, form) {
                        if (form.message && lb_integrate_instance.lb_chat_id) {
                            lb_integrate_instance.send(lb_integrate_instance.lb_chat_id, form.message)
                            self.fluids = [
                                 {
                                    type: "text:text",
                                    value: "Отправка сообщения"
                                }
                            ]
                        } else {
                            lb_integrate_instance.lb_chat_id = 0;
                            self.close()
                        }
                    },
                });
            })



            socket.emit("stream_payment_methods", { passport })
            socket.emit("stream_localbitcoins_update_props", { passport })

        },
    });

    window.binance_integrate_instance = new Vue({
        el: "#binance_integrate_vue",
        data: {
            price: {
                BTCUSDT: 0,
                LTCRUB: 0,
                ETHRUB: 0,
                USDTRUB: 0,
            }
        },
        methods: {
            auth: function () {
                modal_instance.create({
                    title: "Авторизация в Binance",
                    fluids: [
                        {
                            type: "input:text",
                            placeholder: "API ключ",
                            name: "apikey",
                        },
                        {
                            type: "input:text",
                            placeholder: "API секрет",
                            name: "apisecret",
                        },
                    ],
                    submit: function (self, form) {
                        socket.emit("stream_integrate_binance_auth", {
                            form: form,
                            passport,
                        });
                    },
                });
            },
            currency: function (x) {
                return (new Intl.NumberFormat('ru-RU').format(x))
            }
        },
        mounted: function () {
            setInterval(() => {
                socket.emit("stream_binance_price", {passport});
            }, 1000);

            socket.on("stream_binance_price", (price) => {
                this.price[price.symbol] = price.price;
            });
        }
    });

    window.notification_instance = new Vue({
        el: "#notification_vue",
        data: {
            list: []
        },
        methods: {},
        mounted: function () {
            socket.on("emit_new_notification", (data) => {
                this.list.push(data)
                audio.new_notification.play()

                setTimeout(() => {this.list.shift()}, 5000)
            });
        },
    });

    window.toast_instance = new Vue({
        el: "#toast_vue",
        data: {
            list: []
        },
        mounted: function () {
            socket.on("emit_new_toast", (data) => {
                this.list.push(data)
                setTimeout(() => {this.list.shift()}, 5000)
            });
        },
    });


    socket.on("stream_rebooted", (data) => {
        setTimeout(() => {
            document.location.reload()
        }, 2000)
    })

    socket.on("stream_request_reboot", (data) => {
        if ("message" in data) {
            modal_instance.close()
            modal_instance.create({
                title: "Требуется перезагрузка",
                fluids: [
                    {
                        type: "text:text",
                        value: data.message,
                        name: "text",
                    }
                ],
                submit: function (self, form) {
                    socket.emit("stream_accept_reboot", {
                        passport,
                    });
                },
            });
        }
    });

    setInterval((data) => {
        socket.emit("stream_toastnotify_transfer", {
                        passport,
                    });

    }, 1000)



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
