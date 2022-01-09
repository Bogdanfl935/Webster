"use strict";

$(document).ready(() => {
    initArchiveHandlers();
});

function initArchiveHandlers() {
    enableTooltips();
}

function enableTooltips(){
    $("[data-toggle='tooltip']").tooltip();
}