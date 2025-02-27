Vue.createApp({
    name: "App",
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            schema1: {
                lvls: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' количество уровней';
                },
                form: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' форму торта';
                },
                topping: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' топпинг';
                }
            },
            schema2: {
                name: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' имя';
                },
                phone: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' телефон';
                },
                name_format: (value) => {
                    const regex = /^[a-zA-Zа-яА-Я]+$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат имени нарушен';
                    }
                    return true;
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                phone_format:(value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' почту';
                },
                address: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' адрес';
                },
                date: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' дату доставки';
                },
                time: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' время доставки';
                }
            },
            DATA: JSON.parse(document.getElementById("DATA").textContent),
            Costs: JSON.parse(document.getElementById("Costs").textContent),
            Levels: 0,
            Form: 0,
            Topping: 0,
            Berries: 0,
            Decor: 0,
            Words: '',
            Comments: '',
            Designed: false,

            Name: '',
            Phone: null,
            Email: null,
            Address: null,
            Dates: null,
            Time: null,
            DelivComments: ''
        }
    },
    methods: {
        ToStep4() {
            this.Designed = true
            setTimeout(() => this.$refs.ToStep4.click(), 0);
        },

        getCSRFToken() {
            return document
              .querySelector('meta[name="csrf-token"]')
              .getAttribute("content");
          },

        async submitForm() {
            try {
                const csrfToken = this.getCSRFToken();
                const DATA = JSON.parse(document.getElementById("DATA").textContent);
                const requestData = JSON.stringify({
                    cake: {
                        layers: DATA.Levels[this.Levels],
                        shape: DATA.Forms[this.Form],
                        topping: DATA.Toppings[this.Topping],
                        berries: DATA.Berries[this.Berries],
                        decor: DATA.Decors[this.Decor],
                        inscription: this.Words,
                    },
                    comment: this.Comments,
                    customer_name: this.Name,
                    phone_number: this.Phone,
                    email: this.Email,
                    address: this.Address,
                    desired_date: this.Dates,
                    desired_time: this.Time,
                    deliver_comment: this.DelivComments,
                    total_cost: this.Cost
                });

                $.ajax({
                    url: "register_order/",
                    type: "POST",
                    contentType: "application/json",
                    headers: { "X-CSRFToken": csrfToken },
                    data: requestData,
                    success: () => {
                        console.log("Успешная создан заказ:", requestData);
                    },
                    error: (xhr) => {
                      console.error(
                        "Ошибка отправки заказа:",
                        xhr.responseJSON?.error || "Ошибка сети"
                      );
                    },
                  });

            } catch (error) {
                console.error('Error form:', error);
            }
        }
    },
    computed: {
        Cost() {
            let W = this.Words ? this.Costs.Words : 0
            return this.Costs.Levels[this.Levels] + this.Costs.Forms[this.Form] +
                this.Costs.Toppings[this.Topping] + this.Costs.Berries[this.Berries] +
                this.Costs.Decors[this.Decor] + W
        }
    }
}).mount('#VueApp')