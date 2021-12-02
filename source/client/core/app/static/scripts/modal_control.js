"use strict";

$(document).ready(() => {
    initModalControlHandlers();
    launchPopupModals();
});

function initModalControlHandlers() {
    bind_togglers();
}

function launchPopupModals(){
    $(".popup-on-launch").modal("show");
}

function bind_togglers() {
    $("div[data-toggle-group]").each((_div_index, div_element)=>{
        let data_toggle_group_condition = "[data-toggle-group=" + $(div_element).attr("data-toggle-group") + "]"
        let data_toggler_condition = "[data-toggler=" + $(div_element).attr("data-togglee") + "]"
        $("button" + data_toggle_group_condition + data_toggler_condition).each((_button_index, button_element)=>{
            console.log("Binding for: ", div_element, button_element, data_toggle_group_condition);
            $(button_element).on("click", ()=>{
                toggle_target(button_element, div_element, data_toggle_group_condition);
            });
        });
    });
}

function toggle_target(toggler, toggle_target, toggle_group_condition){
    if($(toggle_target).hasClass("d-none")){
        $(toggle_target).fadeIn('slow').removeClass("d-none").addClass("d-block");
        $(toggler).removeClass("btn-dark").addClass("btn-light");
        $("button" + toggle_group_condition).each((_index, button_element)=>{
            if(button_element != toggler){
                $(button_element).removeClass("btn-light").addClass("btn-dark");
            }
        });
        $("div" + toggle_group_condition).each((_index, div_element)=>{
            if(div_element != toggle_target){
                $(div_element).fadeOut("slow").removeClass("d-block").addClass("d-none");
            }
        });
    }
}