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
        $(form).on('submit', (event) => { formSubmitHandler(event, form) });
    });
}

function formSubmitHandler(event, form) {
    event.preventDefault();
    if (!$(form).valid()) {
        event.stopPropagation()
    }
    else {
        makeFormAjaxCall(form);
    }
    $(form).find("input[required]").addClass('was-validated');
}

function makeFormAjaxCall(form) {
    $.ajax({
        type: $(form).attr('method'),
        url: $(form).attr('action'),
        data: $(form).serialize(),
        success: (data) => { handleFormSubmitSuccessResponse(form, data); },
        error: (data) => { handleFormSubmitErrorResponse(form, data); }
    });
}

function handleFormSubmitSuccessResponse(form, response) {
    form.reset();
    $(form).find("input[required]").removeClass('was-validated');
    if (response.redirect === true) {
        window.location.replace(response.url);
    }
}

function handleFormSubmitErrorResponse(form, response) {
    if (response.responseJSON.redirect === true) {
        window.location.href = response.responseJSON.url;
    }
    else if ([400, 401, 409].includes(response.status)) {
        let prevSibling = $(form).find("button").prev("div[class*='error-feedback']");
        if (prevSibling.length == 0) {
            let invalidSpan = document.createElement("span");
            prevSibling = document.createElement("div");
            $(prevSibling).addClass("col-12 mb-3 error-feedback");
            $(invalidSpan).addClass("invalid-feedback d-block");
            prevSibling.appendChild(invalidSpan);
            $(form).find("button").before(prevSibling);
        }

        $(prevSibling).children().first().text(response.responseJSON.error);
    }
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