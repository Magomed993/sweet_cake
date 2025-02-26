Vue.createApp({
  components: {
    VForm: VeeValidate.Form,
    VField: VeeValidate.Field,
    ErrorMessage: VeeValidate.ErrorMessage,
  },
  data() {
    return {
      RegSchema: {
        reg: (value) => {
          if (value) {
            return true;
          }
          return "Поле не заполнено";
        },
        phone_format: (value) => {
          const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/;
          if (!value) {
            return true;
          }
          if (!regex.test(value)) {
            return "⚠ Формат телефона нарушен";
          }
          return true;
        },
        code_format: (value) => {
          const regex = /^[a-zA-Z0-9]+$/;
          if (!value) {
            return true;
          }
          if (!regex.test(value)) {
            return "⚠ Формат кода нарушен";
          }
          return true;
        },
      },
      Step: "Number",
      RegInput: "",
      EnteredNumber: "",
    };
  },
  methods: {
    getCSRFToken() {
      return document
        .querySelector('meta[name="csrf-token"]')
        .getAttribute("content");
    },

    RegSubmit(event) {
      const csrfToken = this.getCSRFToken();

      if (this.Step === "Number") {
        $.ajax({
          url: "/login/",
          type: "POST",
          contentType: "application/json",
          headers: { "X-CSRFToken": csrfToken },
          data: JSON.stringify({ phone: this.RegInput }),
          success: () => {
            this.Step = "Code";
            this.EnteredNumber = this.RegInput;
            this.RegInput = "";
          },
          error: (xhr) => {
            console.error(
              "Ошибка отправки кода:",
              xhr.responseJSON?.error || "Ошибка сети"
            );
          },
        });
      } else if (this.Step === "Code") {
        $.ajax({
          url: "/login/",
          type: "POST",
          contentType: "application/json",
          headers: { "X-CSRFToken": csrfToken },
          data: JSON.stringify({
            phone: this.EnteredNumber,
            code: this.RegInput,
          }),
          success: (data) => {
            console.log("Успешная авторизация:", data);
            this.Step = "Finish";
            this.RegInput = "Регистрация успешна";
            setTimeout(() => {
              location.reload();
            }, 1000);
          },
          error: (xhr) => {
            console.error(
              "Ошибка проверки кода:",
              xhr.responseJSON?.error || "Ошибка сети"
            );
          },
        });
      }
    },

    ToRegStep1() {
      this.Step = "Number";
      this.RegInput = this.EnteredNumber;
    },

    Reset() {
      this.Step = "Number";
      this.RegInput = "";
      this.EnteredNumber = "";
    },
  },
}).mount("#RegModal");
