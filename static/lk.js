Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        const Client = JSON.parse(document.getElementById("client").textContent);        
        return {
            Edit: false,
            Name: Client.customer_name,
            Phone: Client.phone_number,
            Email: Client.email,
            Schema: {
                name_format: (value) => {
                    const regex = /^[a-zA-Zа-яА-я]+$/
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Недопустимые символы в имени';
                    }
                    return true;
                },
                phone_format: (value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                }
            }
        }
    },
    methods: {
        getCSRFToken() {
            return document
              .querySelector('meta[name="csrf-token"]')
              .getAttribute("content");
          },
          
        ApplyChanges() {
            this.Edit = false

            try {
                const csrfToken = this.getCSRFToken();
                const requestData = JSON.stringify({
                    customer_name: this.Name,
                    phone_number: this.Phone,
                    email: this.Email,
                });

                $.ajax({
                    url: "change_profile/",
                    type: "POST",
                    contentType: "application/json",
                    headers: { "X-CSRFToken": csrfToken },
                    data: requestData,
                    success: (response) => {
                        console.log(response);
                    },
                    error: (xhr) => {
                      console.error(
                        "Ошибка изменения профиля:",
                        xhr.responseJSON?.error || "Ошибка сети"
                      );
                    },
                  });

            } catch (error) {
                console.error('Error profile:', error);
            }
            
            this.$refs.HiddenFormSubmit.click()
        }
    }
}).mount('#LK')