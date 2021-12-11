"use strict";

const MILLISECONDS = 1;
const SECONDS = MILLISECONDS * 1000;
const MINUTES = SECONDS * 60;
const HOURS = MINUTES * 60;
const DAYS = HOURS * 24;
const YEARS = DAYS * 365;

$(document).ready(() => {
    initActivityHandlers();
});

function initActivityHandlers() {
    enableTooltips();
    //startElapsedTimeCounter();
    //enableCrawlerStatusPolling();
}

function enableCrawlerStatusPolling(){
    let pollingFrequency = 1000 * MILLISECONDS;
    let continuePolling = true;
    let intervalHandle = setInterval(()=>{
        if(continuePolling){
            makeAjaxRequest($("#crawlerStatusForm"), handleStatusFormSubmitSuccessResponse, (form, data)=>{console.log(data)});
        }
        else{
            clearInterval(intervalHandle);
        }
        
    }, pollingFrequency);
}

function makeAjaxRequest(form, success_handle, error_handle){
    $.ajax({
        type: $(form).attr('method'),
        url: $(form).attr('action'),
        data: $(form).serialize(),
        success: (data) => { success_handle(form, data); },
        error: (data) => { 
            if (data.responseJSON) {
                error_handle(form, data);
            }
        }
    });
}

function handleStatusFormSubmitSuccessResponse(form, data){
    $("#crawlerMemoryUsage span").text((parseFloat(data.memoryUsage)/1024).toFixed(2).toString()+"kB");
    $("#crawlerCurrentCrawl").text(data.domain).attr("data-bs-original-title", data.url);
}

function enableTooltips(){
    $("[data-toggle='tooltip']").tooltip();
}

function startElapsedTimeCounter(){
    const newDateTime = new Date();
    setInterval(()=>{
        $("#elapsedTimeCounter").text(computeElapsedTime(newDateTime));
    }, 1000);
}

function computeElapsedTime(referenceTime){
    const newDateTime = new Date();
    let elapsedMilliseconds=  newDateTime - referenceTime;
    return formatElapsedTime(elapsedMilliseconds, DAYS) + "d "
        + formatElapsedTime(elapsedMilliseconds, HOURS, 24) + "h "
        + formatElapsedTime(elapsedMilliseconds, MINUTES, 60) + "m "
        + formatElapsedTime(elapsedMilliseconds, SECONDS, 60) + "s"
}

function formatElapsedTime(elapsedtime, timeunit, base) {
  let time = base ? (elapsedtime / timeunit) % base : elapsedtime / timeunit;
  time = Math.floor(time);
  time = time < 10 ? '0' + time : time;
  return time;
}