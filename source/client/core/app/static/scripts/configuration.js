"use strict";

$(document).ready(() => {
    initConfigurationHandlers();
});

function initConfigurationHandlers() {
    bindButtonClickEvents();
    bindContentEditableHandler();
    bindInitialRemoveHandlers();
}

function bindInitialRemoveHandlers(){
    $("span[class='tag-remove-span']").each((_index, elem)=>{
        $(elem).one("click", function(_event) {
            handleTagDeletion($(this).parent().prev().find("span"));
        });
    });
}

function bindContentEditableHandler(){
    $("span[contenteditable]").last().on('keypress paste', function(event) {
        /* If enter, submit */
        if(event.keyCode == 13){
            $(this).off('focusout');
            handleTagInsertion(this);
        }
        /* If invalid character OR length over 32, prevent writing */
        else if(String.fromCharCode(event.keyCode).match(/[\-\w]/gi) === null || 
            $(this).text().length >= 32 && ![8, 37, 39].includes(event.keyCode)) { 
          event.preventDefault();
        }
    });
    /* If focus is lost, submit */
    $("span[contenteditable]").last().one('focusout', function(_event){
        handleTagInsertion(this);
    });
}

function handleTagInsertion(tag_element){
    rebindAndSubmitTagForm($(tag_element).text(), "POST");
    $(tag_element).removeAttr('contenteditable');
    $(tag_element).blur();
}

function handleTagDeletion(tag_element){
    rebindAndSubmitTagForm($(tag_element).text(), "DELETE");
    $(tag_element).parents().eq(3).remove();
}

function rebindAndSubmitTagForm(tag_value, method){
    let form = $('#parserConfigurationForm');
    $(form).find("input[type=hidden]").val(tag_value);
    $(form).attr("action", method == "POST" ? $(form).attr("action") : $(form).attr("alternative_action"));
    form.on('submit', (event) => {
        event.preventDefault();
        formSubmitHandler(
            event, 
            form,
            ()=>{}, /* Success handle, do nothing */
            (_form, data)=>{console.log(data);} /* Error handle */
        );
    });
    form.submit();
}

function focusTag(){
    let tagSpan = $("span[contenteditable]").last();
    $(tagSpan).focus();
    let windowSelection = window.getSelection();
    let range = document.createRange();
    range.setStart($(tagSpan).get(0), 0);
    range.setEnd($(tagSpan).get(0), 0);
    windowSelection.removeAllRanges();
    windowSelection.addRange(range);
}

function bindButtonClickEvents(){
    $("#tagInsertionButton").click(handleInsertionClickEvent);
}

function bindRemoveHandler(){
    let tagSpan = $("span[contenteditable]").last();
    $("span[class='tag-remove-span']").last().one('click', function(_event){
        handleTagDeletion(tagSpan);
    });
}

function handleInsertionClickEvent(){
    $(".parser-tags-container").append(renderNewTag())
    bindContentEditableHandler();
    bindRemoveHandler();
    focusTag();
}

function renderNewTag(){
    return `<div class="col-md-3 mx-1 card">
        <div class="row">
            <div class="col-lg-10 col-10 col-sm-11 card-body overflow-hidden">
                <kbd>&lt;<span contenteditable maxlength=32 spellcheck=false></span>&gt;</kbd> 
            </div>
            <div class="col-lg-2 col-2 col-sm-1 card-body">
                <span role="button" class="tag-remove-span"><i class="fas fa-trash-alt text-danger"></i></span>
            </div>
        </div>
    </div>`
}
