var CREATE_PROJECT_SELECTOR = '[data-form-role="field"]';
var SHOW_FORM_CLASS = 'container';
var ALERT_CLASS = 'alert alert-danger';

function addProject() {
    'use strict';
    document.getElementById('newProject').addEventListener('click', function (event) {
        event.preventDefault();
        var formField = document.querySelector(CREATE_PROJECT_SELECTOR);
        formField.setAttribute('class', SHOW_FORM_CLASS);
    });
}

// function deleteProject() {
//     'use strict';
//     document.getElementById('deleteProject').addEventListener('click', function (event) {
//         event.preventDefault();
//         var div = document.createElement("div");
//         var text = document.createElement("p");
//         var message = document.createTextNode('Are you sure you want to delete this project?');
//         text.appendChild(message);
//         div.appendChild(text);
//         var ok = document.createElement("button");
//         var okText = document.createTextNode('Delete');
//         ok.appendChild(okText);
//         ok.setAttribute('class','btn-default btn-sm')
//         var notOk = document.createElement('button');
//         var notOkText = document.createTextNode('Cancel');
//         notOk.appendChild(notOkText);
//         notOk.setAttribute('class','btn-default btn-sm')
//         div.setAttribute('class', ALERT_CLASS);
//         div.appendChild(ok);
//         div.appendChild(notOk);
//         var anchor = document.getElementById('firstDiv');
//         document.body.insertBefore(div,anchor);
//     });
// }

function initializeEvents() {
    addProject();
    // deleteProject();
}

initializeEvents();
