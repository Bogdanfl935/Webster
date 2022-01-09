"use strict";

$(document).ready(() => {
    initHomeHandlers();
});

function initHomeHandlers() {
    renderStatistics();
}

function renderStatistics(){
    let form = $('#statisticsForm');
    submitFormByAction(form, $(form).attr("action"), constructChart);
    submitFormByAction(form, $(form).attr("alternative-action"), renderCardParameters);
    $(form).remove();
}

function submitFormByAction(form, action, callback){
    $(form).attr("action", action);
    form.on('submit', (event) => {
        event.preventDefault();
        formSubmitHandler(
            event, 
            form,
            (_form, data)=>{callback(data)}, /* Success handle */
            (_form, data)=>{console.log(data);} /* Error handle */
        );
    });
    form.submit();
}

function unpackChartSettings(data){
    const processedData = data.map((dataEntry)=>{
        return {
            toolTipContent: dataEntry.url, 
            label: _getHostName(dataEntry.url), 
            y: dataEntry.count
        };
    });
    return {
        theme: "light1",
        animationEnabled: true,
        exportEnabled: true,
        axisX: {
            margin: 10,
            labelPlacement: "inside",
            tickPlacement: "inside",
            labelFontColor: "white"
        },
        axisY2: {
            titleFontSize: 14,
            includeZero: true
        },
        data: [{
            type: "bar",
            axisYType: "secondary",
            indexLabel: "{y}",
            dataPoints: processedData
        }]
    };
}

function constructChart(data){
    const chartSettings = unpackChartSettings(data);
    new CanvasJS.Chart("chartContainer", chartSettings).render();
}

function renderCardParameters(data){
    $("h3[class='h3-right']").each((index, elem)=>{
        $(elem).val(data[index]);
    });
}

function _getHostName(url){
    let anchor = document.createElement('a');
    anchor.href = url;
    return anchor.hostname;
}

