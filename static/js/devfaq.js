document.body.addEventListener('htmx:beforeRequest', function(evt) {
    let form_submit = document.querySelector('#submit_form');
    form_submit.disabled = true;
});

document.body.addEventListener('htmx:beforeSwap', function(evt) {
    evt.detail.shouldSwap = false;
    reset_form();
    const response = JSON.parse(evt.detail.xhr.response);
    if (response.result === 'failed'){
        process_failures(response.errors);
    }
    if (response.result === 'success'){
        window.location.replace(response.redirect_url);
    }
});

function process_failures(errors){
    for (let error in errors){
        // TODO handle displaying the global errors
        // TODO handle adding a float to display errors for fields
        let element = document.getElementById('id_' + error);
        element.classList.add('input_error');
    }
}

function reset_form(){
    let errors = document.getElementsByClassName('input_error');
    for (let i = 0;i < errors.length; i++) {
        errors[0].classList.remove('input_error');
    }
    let form_submit = document.querySelector('#submit_form');
    form_submit.disabled = false;
}
