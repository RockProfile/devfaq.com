document.body.addEventListener('htmx:beforeRequest', function(evt) {
    /*
    Listens for HTMX events prior to an AJAX request.

    Args:
        evt: The triggered event
     */
    let verb = evt.detail.elt.verb;
    if (verb !== "post"){
        return;
    }
    let form_submit = document.querySelector('#submit_form');
    form_submit.disabled = true;
});

document.body.addEventListener('htmx:beforeSwap', function(evt) {
    /*
    Listens for HTMX events prior to swapping content.

    Args:
        evt: The triggered event
     */
    let response = ''
    try {
        response = JSON.parse(evt.detail.xhr.response);
    } catch (e) {
        return;
    }
    evt.detail.shouldSwap = false;
    reset_form();

    if (response.result === 'failed'){
        process_failures(response.errors);
        return;
    }
    if (response.result === 'success' && len(response.content) === 0){
        window.location.replace(response.redirect_url);
    }
    else if (response.result === 'success' && len(response.content) === 0){
        evt.detail.shouldSwap = true;
    }
});

function process_failures(errors){
    /*
    Process for errors.

    Args:
        errors: List of errors
     */
    for (let error in errors){
        // TODO handle displaying the global errors
        // TODO handle adding a float to display errors for fields
        let element = document.getElementById('id_' + error);
        element.classList.add('is-invalid');
    }
}

function reset_form(){
    /*
    Reset a form to remove formatting and errors.
     */
    let errors = document.getElementsByClassName('is-invalid');
    for (let i = 0;i < errors.length; i++) {
        errors[0].classList.remove('is-invalid');
    }
    let form_submit = document.querySelector('#submit_form');
    form_submit.disabled = false;
}
