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
    bindCrawlerStopFormSubmitHandle();
}

function bindCrawlerStopFormSubmitHandle(){
    let form = $('#crawlerStopForm');
    form.on('submit', (event) => {
        formSubmitHandler(
            event, 
            form,
            () => {}, /* Do nothing */
            (_form, data)=>{console.log(data); location.reload();}, /* Error handle */
            () => {$(form).find("input[required]").addClass('was-validated');} /* Callback */
        );
    });
}

function enableCrawlerStatusPolling(){
    let pollingFrequency = 1000 * MILLISECONDS;
    let continuePolling = true;
    makeAjaxRequest($("#crawlerStatusForm"), handleCrawlerStatusFormSubmitSuccessResponse, (form, data)=>{console.log(data)});
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
    renderParserTableContent(data, tableBody);
    enableTooltips();
}

function renderParserTableContent(data, tableBody){
    let rowsCount = $('#parserStatusTable tr').length;
    Object.keys(data).forEach((dict_key, _)=>{
        data[dict_key].forEach((entry, _)=>{
            let col_1 = `<th class="col-md-1" scope="row">${rowsCount++}</th>`
            let col_2 = `<td class="col-md-1"><span class="badge badge-dark">&lt;${entry.tag}&gt;</span></td>`
            let col_3 = `<td class="col-md-1"><span class="badge badge-danger">${(entry.memoryUsage/1024).toFixed(2)+"kB"}</span></td>`
            let col_4 = `<td class="col-md-1"><span class="badge badge-info" role='button' data-toggle="tooltip"
            data-placement="bottom" title="${dict_key}">${_getHostName(dict_key)}</span></td>`
            tableBody.prepend(`<tr>${col_1}${col_2}${col_3}${col_4}</tr>`);
        });
    });
}

function handleCrawlerStatusFormSubmitSuccessResponse(form, data){
    if(data.active == true){
        $("#crawlerMemoryUsage span").text((parseFloat(data.memoryUsage)/1024).toFixed(2).toString()+"kB");
        $("#crawlerCurrentCrawl").text(_getHostName(data.lastUrl)).attr("data-bs-original-title", data.lastUrl);
    }
    else{
        location.reload();
    }
    
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

function _getHostName(url){
    let anchor = document.createElement('a');
    anchor.href = url;
    return anchor.hostname;
}