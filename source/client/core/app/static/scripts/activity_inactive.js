"use strict";

$(document).ready(() => {
    initActivityHandlers();
});

function initActivityHandlers() {
    
}

function bindCrawlerStartFormSubmitHandle(){
    let form = $('#crawlerStartForm');
    form.on('submit', (event) => {
        formSubmitHandler(
            event, 
            form,
            handleParserStatusFormSubmitSuccessResponse, /* Success handle */
            (_form, data)=>{console.log(data);} /* Error handle */
        );
    });
}