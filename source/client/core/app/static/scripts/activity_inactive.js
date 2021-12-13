"use strict";

$(document).ready(() => {
    initActivityHandlers();
});

function initActivityHandlers() {
    bindCrawlerStartFormConstraints();
    bindCrawlerStartFormSubmitHandle();
}

function bindCrawlerStartFormSubmitHandle(){
    let form = $('#crawlerStartForm');
    form.on('submit', (event) => {
        formSubmitHandler(
            event, 
            form,
            handleCrawlerStartFormSubmitSuccessResponse, /* Success handle */
            (_form, data)=>{console.log(data); location.reload();}, /* Error handle */
            () => {$(form).find("input[required]").addClass('was-validated');} /* Callback */
        );
    });
}

function bindCrawlerStartFormConstraints(){
    let form = $("#crawlerStartForm");
    createCustomUrlRule();
    $(form).validate({
        rules: {startUrl: { required: true, url: true }},
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

function createCustomUrlRule(){
    $.validator.addMethod(
        "url",
        function (value, element) {
            let input = document.createElement('input');
            input.setAttribute('type', 'url');
            input.value = value;
            return this.optional(element) || input.validity.valid;
        },
        "Please enter a valid URL."
    );
}

function handleCrawlerStartFormSubmitSuccessResponse(form, data){
    location.reload();
}