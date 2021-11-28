"use strict";

$(document).ready(() => {
    initHandlers();
});

function initHandlers() {
    bindShowHideClickHandler();
    bindModalContentToggleHandler();
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
    let loginButtonMap = { buttonId: '#login-toggler', modalContentId: '#login-modal-content', target: null};
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
        $(form).on('submit', (event) => {
            event.preventDefault();
            makeFormAjaxCall(form);
        });
    });
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
    if (response.redirect === true) {
        window.location.replace(response.url);
    }
}

function handleFormSubmitErrorResponse(form, response) {
    if (response.responseJSON.redirect === true) {
        window.location.replace(response.responseJSON.url);
    }
    else if ([400, 401, 409].includes(response.status)) {
        let prevSibling = $(form).find("button").prev();
        if (prevSibling.length == 0) {
            prevSibling = document.createElement("span");
            $(form).find("button").before(prevSibling);
        }

        prevSibling.innerText = response.responseJSON.error;
    }
}