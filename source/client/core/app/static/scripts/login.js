"use strict";

$(document).ready(() => {
    initHandlers();
});

function initHandlers() {
    bindShowHideClickHandler();
    bindModalContentToggleHandler();
    bindFormValidationHandler();
    bindFormSubmitHandler();
}

function bindShowHideClickHandler() {
    $(".show-hide-password").on('click', (event) => {
        if ($(event.currentTarget).next().attr("type") == "text") {
            $(event.currentTarget).next().attr('type', 'password');
            $(event.currentTarget).find("div").find("i").addClass("fa-eye-slash");
            $(event.currentTarget).find("div").find("i").removeClass("fa-eye");
        } else if ($(event.currentTarget).next().attr("type") == "password") {
            $(event.currentTarget).next().attr('type', 'text');
            $(event.currentTarget).find("div").find("i").removeClass("fa-eye-slash");
            $(event.currentTarget).find("div").find("i").addClass("fa-eye");
        }
    });
}

function bindModalContentToggleHandler() {
    let loginButtonMap = { buttonId: '#login-toggler', modalContentId: '#login-modal-content', target: null };
    let registerButtonMap = { buttonId: '#register-toggler', modalContentId: '#register-modal-content', target: null };
    loginButtonMap.target = registerButtonMap;
    registerButtonMap.target = loginButtonMap;

    let buttonMapList = [loginButtonMap, registerButtonMap];
    let active = true;

    for (let buttonMapIndex in buttonMapList) {
        $(buttonMapList[buttonMapIndex].buttonId).on('click', () => {
            if ($(buttonMapList[buttonMapIndex].modalContentId).hasClass("d-none")) {
                toggleModalContent(buttonMapList[buttonMapIndex], active);
                toggleModalContent(buttonMapList[buttonMapIndex].target, !active);
            }
        });
    }
}

function toggleModalContent(modalButtonMap, setActive) {
    if (setActive === true) {
        $(modalButtonMap.modalContentId).removeClass("d-none");
        $(modalButtonMap.modalContentId).addClass("d-block");

        $(modalButtonMap.buttonId).removeClass("btn-dark");
        $(modalButtonMap.buttonId).addClass("btn-light");
    }
    else {
        $(modalButtonMap.modalContentId).removeClass("d-block")
        $(modalButtonMap.modalContentId).addClass("d-none");

        $(modalButtonMap.buttonId).removeClass("btn-light");
        $(modalButtonMap.buttonId).addClass("btn-dark");
    }
}

function bindFormSubmitHandler() {
    $('form').each((index, form) => {
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
        let prevSibling = $(form).find("button").prev();
        if (prevSibling.length == 0) {
            let invalidSpan = document.createElement("span");
            prevSibling = document.createElement("div");
            $(prevSibling).addClass("col-12 mb-3");
            $(invalidSpan).addClass("invalid-feedback d-block");
            prevSibling.appendChild(invalidSpan);
            $(form).find("button").before(prevSibling);
        }

        $(prevSibling).children().first().text(response.responseJSON.error);
    }
}

function bindFormValidationHandler() {
    createStrongPasswordRule();
    let rules_list = [
        {
            username: { required: true, email: true },
            password: { required: true }
        },
        {
            username: { required: true, email: true },
            password: {required: true, minlength: 8, maxlength: 30, strongPassword: true},
            confirmPassword: { required: true, minlength: 8, maxlength: 30, equalTo: "#registerPassword" }
        }
    ]
    let messages_list = [
        {
            username: "Please enter a valid email address",
            password: "Please provide a password"
        },
        {
            username: "Please enter a valid email address",
            password: {
                required: "Please provide a password"
            },
            confirmPassword: {
                required: "Please provide a password",
                equalTo: "Passwords do not match"
            }
        },
    ]

    $("form").each((index, form) => {
        $(form).validate({
            rules: rules_list[index],
            messages: messages_list[index],
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