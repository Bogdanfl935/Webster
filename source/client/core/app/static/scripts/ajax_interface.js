function formSubmitHandler(
    event, 
    form,
    success_handle = ()=>{}, 
    error_handle = ()=>{}, 
    callback = ()=>{}
) 
{
    event.preventDefault();
    if (!$(form).valid()) {
        event.stopPropagation();
    }
    else {
        makeAjaxRequest(form, success_handle, error_handle);
    }
    callback();
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