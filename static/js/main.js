var FORM_FIELD_SELECTOR = '[data-form-role="field"]';
var CLICK_SELECTOR = '[data-role="clickMe"]';
var HIDDEN_CLASS = 'hidden-field';
var SHOW_FORM_CLASS = 'pop-out-form';


function addClickListener(plus) {
    'use strict';
    plus.addEventListener('click', function (event) {
        event.preventDefault();
        showForm();
    });
}

function showForm() {
    'use strict';
    var field = document.querySelector(FORM_FIELD_SELECTOR);
    document.body.classList.remove(HIDDEN_CLASS)
    field.classList.add(SHOW_FORM_CLASS)
}

function initializeEvents() {
    'user strict';
    var plusButton = document.querySelector(CLICK_SELECTOR)
    addClickListener(plusButton);
}

initializeEvents();
