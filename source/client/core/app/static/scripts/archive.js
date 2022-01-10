"use strict";

$(document).ready(() => {
    initArchiveHandlers();
});

function initArchiveHandlers() {
    enableTooltips();
    bindActionButtonEventHandlers();
}

function enableTooltips(){
    $("[data-toggle='tooltip']").tooltip();
}

function bindActionButtonEventHandlers(){
    bindDeleteHandler();
    bindExportHandler();
}

function bindDeleteHandler(){
    $("span[class*='delete-crawled']").on('click', function(_event){
        const source = $(this).parent().prev().find("span[class*='parsed-content-data']").attr("data-bs-original-title");
        fetch($("#contentControlForm").attr("alternative-action"), {
            method:'DELETE',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({source: source})
        }).then(function(response){
            if(response.status == 200){
                location.reload();
            }
        });
    });
}

function bindExportHandler(){
    $("span[class*='download-crawled']").on('click', function(_event){
        const source = $(this).parent().prev().find("span[class*='parsed-content-data']").attr("data-bs-original-title");
        fetch($("#contentControlForm").attr("action"), {
            method:'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({source: source})
        }).then(function(response){
            console.log(response);
            return response.json();
        }).then((data)=>{
            download("archive.zip", data.parsedContent);
        });
    });
}

function download(filename, data) {
    let element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;base64,' + data);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}
