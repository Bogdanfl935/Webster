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
    $(form).off('submit'); /* Unbind previous submit event handler */
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
    if(data.length > 0){
        const chartSettings = unpackChartSettings(data);
        new CanvasJS.Chart("chartContainer", chartSettings).render();
    }
    else{
        const displayContent = renderNoDataToDisplay();
        $("#chartContainer").html(displayContent);
        $("#chartContainer").height(100);
    }
}

function renderCardParameters(data){
    const convertedMemoryUsage = (parseFloat(data.memoryUsage)/(1024*1024)).toFixed(4).toString();
    const dataMapping = [convertedMemoryUsage, data.totalParsedUrls, data.visitedUrls];
    $("h3[class*='statistics-container'] span").each((index, elem)=>{
        $(elem).text(dataMapping[index]);
    });
}

function renderNoDataToDisplay(){
    return `
    <div class="mdl-card__supporting-text">
        <div class="row py-2 px-3">
            <span class="lead">No statistics available. Start crawler to update activity</span>
        </div>
    </div>`
}

function _getHostName(url){
    let anchor = document.createElement('a');
    anchor.href = url;
    return anchor.hostname;
}

