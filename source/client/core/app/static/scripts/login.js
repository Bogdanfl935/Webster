"use strict";

$(document).ready(() => {
    initAuthenticationModalHandlers();
});

function initAuthenticationModalHandlers() {
    bindShowHideClickHandler();
    bindAuthenticationFormConstraints();
    bindRegistrationFormConstraints();
    bindFormSubmitHandler();
}

function bindShowHideClickHandler() {
    $(".show-hide-password").on('click', (event) => {
        if ($(event.currentTarget).next().attr("type") == "text") {
            $(event.currentTarget).next().attr('type', 'password');
            $(event.currentTarget).find("div i").addClass("fa-eye-slash").removeClass("fa-eye");
        } else if ($(event.currentTarget).next().attr("type") == "password") {
            $(event.currentTarget).next().attr('type', 'text');
            $(event.currentTarget).find("div i").removeClass("fa-eye-slash").addClass("fa-eye");
        }
    });
}

function bindFormSubmitHandler() {
    $('form[class*="ajax-handled"]').each((index, form) => {
        $(form).on('submit', (event) => { 
            formSubmitHandler(
                event, 
                form,
                handleFormSubmitSuccessResponse, /* Success handle */
                handleFormSubmitErrorResponse, /* Error handle */
                () => {$(form).find("input[required]").addClass('was-validated');} /* Callback */
            );
        });
    });
}

function handleFormSubmitSuccessResponse(form, response) {
    form.reset();
    $(form).find("input[required]").removeClass('was-validated');
    if (response.url != null) {
        window.location.replace(response.url);
    }
    else if(response.renderModalTemplate != null){
        renderFeedbackModalTemplate(response.renderModalTemplate);
    }
}

function handleFormSubmitErrorResponse(form, response) {
    if (response.responseJSON.url != null) {
        window.location.href = response.responseJSON.url;
    }
    else if(response.responseJSON.renderModalTemplate != null){
        renderFeedbackModalTemplate(response.responseJSON.renderModalTemplate);
    }
    else {
        switch (response.status) {
            case 400:
                ajaxHandle400Response(form, response.responseJSON.error);
                break;
            case 401:
                // Intentional fall-through
            case 403:
                // Intentional fall-through
            case 409:
                ajaxHandle401_403_409Response(form, response.responseJSON.error);
                break;
            default:
                break;
        }   
    }
}

function ajaxHandle400Response(form, error_list){
    $(error_list).each((_index, error_json) => {
        $(form).find("input[name=" + error_json.fieldName + "]").each((_index, input_field) => {
            let feedback_label = $(input_field).next("label[class*='invalid-feedback']");
            if (feedback_label.length == 0) {
                let feedback_label = document.createElement("label");
                $(feedback_label).addClass("invalid-feedback");
                $(input_field).after(feedback_label);
            }
            $(feedback_label).text(error_json.errorMessage);
        });
    });
    $(form).addClass("is-invalid");
}

function ajaxHandle401_403_409Response(form, error_message){
    let prevSibling = $(form).find("button").prev("div[class*='error-feedback']");
    if (prevSibling.length == 0) {
        let invalidSpan = document.createElement("span");
        prevSibling = document.createElement("div");
        $(prevSibling).addClass("col-12 mb-3 error-feedback");
        $(invalidSpan).addClass("invalid-feedback d-block");
        prevSibling.appendChild(invalidSpan);
        $(form).find("button").before(prevSibling);
    }
    $(prevSibling).children().first().text(error_message);
}

function bindFormValidationHandler(form, rules, messages) {
    $(form).validate({
        rules: rules,
        messages: messages,
        errorPlacement: function (error, element) {
            error.addClass('invalid-feedback');
            element.closest('.input-group').append(error);
        },
        highlight: function (element) {
            $(element).addClass('is-invalid');
            element.setCustomValidity('Invalid');
        },
        unhighlight: function (element) {
            $(element).removeClass('is-invalid');
            element.setCustomValidity('');
        },
    });
}

function bindRegistrationFormConstraints(){
    createStrongPasswordRule();
    let registration_rules = {
            username: { required: true, email: true },
            password: { required: true, minlength: 8, maxlength: 30, strongPassword: true },
            confirmPassword: { required: true, minlength: 8, maxlength: 30}
    };
    let registration_messages = {
        username: "Please enter a valid email address",
        password: { required: "Please provide a password" },
        confirmPassword: {
            required: "Please provide a password",
            equalTo: "Passwords do not match"
        }
    };
    $("form[data-form-type=registration]").each((_index, form)=>{
        registration_rules.confirmPassword.equalTo = $(form).find("input[name=password]");
        bindFormValidationHandler(form, registration_rules, registration_messages);
    });
}

function bindAuthenticationFormConstraints(){
    let authentication_rules = {
        username: { required: true, email: true },
        password: { required: true }
    };
    let authentication_messages = {
        username: "Please enter a valid email address",
        password: "Please provide a password"
    };
    $("form[data-form-type=authentication]").each((_index, form)=>{
        bindFormValidationHandler(form, authentication_rules, authentication_messages);
    });
}

function createStrongPasswordRule(){
    $.validator.addMethod(
        "strongPassword",
        function (value, element) {
            let regexp = "^((?=.*[!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~])(?=.*[0-9])(?=.*[A-Z])|(?=.*[!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~])(?=.*[0-9])(?=.*[a-z])|(?=.*[!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~])(?=.*[A-Z])(?=.*[a-z])|(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]))[a-zA-Z0-9!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~]+$";
            return this.optional(element) || new RegExp(regexp).test(value);
        },
        "Password must contain three out of the four: lowercase letter, uppercase letter, digit or special character"
    );
}