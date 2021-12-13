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
    startElapsedTimeCounter();
    enableCrawlerStatusPolling();
    bindParserFormSubmitHandle();
}

function enableCrawlerStatusPolling(){
    let pollingFrequency = 1000 * MILLISECONDS;
    let continuePolling = true;
    let intervalHandle = setInterval(()=>{
        if(continuePolling){
            makeAjaxRequest($("#crawlerStatusForm"), handleCrawlerStatusFormSubmitSuccessResponse, (form, data)=>{console.log(data)});
        }
        else{
            clearInterval(intervalHandle);
        }
        
    }, pollingFrequency);
}

function bindParserFormSubmitHandle(){
    let form = $('#parserStatusForm');
    form.on('submit', (event) => {
        formSubmitHandler(
            event, 
            form,
            handleParserStatusFormSubmitSuccessResponse, /* Success handle */
            (_form, data)=>{console.log(data);} /* Error handle */
        );
    });
}

function handleParserStatusFormSubmitSuccessResponse(_form, data){
    let tableBody = $('#parserStatusTable');
    tableBody.empty();
    data.content.forEach((entry, index)=>{
        let col_1 = `<th class="col-md-1" scope="row">${index}</th>`
        let col_2 = `<td class="col-md-1"><span class="badge badge-dark">&lt;${entry.tag}&gt;</span></td>`
        let col_3 = `<td class="col-md-1"><span class="badge badge-danger">${(entry.size/1024).toFixed(2)+"kB"}</span></td>`
        let col_4 = `<td class="col-md-1"><span class="badge badge-info" role='button' data-toggle="tooltip"
        data-placement="bottom" title="${data.url}">${data.domain}</span></td>`
        tableBody.append(`<tr>${col_1}${col_2}${col_3}${col_4}</tr>`);
    });
    enableTooltips();
}

function handleCrawlerStatusFormSubmitSuccessResponse(form, data){
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