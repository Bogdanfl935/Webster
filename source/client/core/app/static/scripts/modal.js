"use strict";

$(document).ready(() => {
    initHandlers();
});

function initHandlers() {
    bindShowHideClickHandler();
    bindModalContentToggleHandler();
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
    let loginButtonMap = { buttonId: '#login-toggler', modalContentId: '#login-modal-content' };
    let registerButtonMap = { buttonId: '#register-toggler', modalContentId: '#register-modal-content' };
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