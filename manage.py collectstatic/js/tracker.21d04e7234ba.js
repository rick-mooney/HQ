var MASS_UPDATE_SELECTOR = '[data-form-role="field"]';
var CHECKBOX_SELECTOR = '[data-form-role="checkbox"]';
var SHOW_FORM_CLASS = 'container';
var CLEAR_ATTR = '#';

function showMassUpdate() {
    'use strict';
    document.getElementById('massUpdate').addEventListener('click', function (event) {
        event.preventDefault();
        var formField = document.querySelector(MASS_UPDATE_SELECTOR);
        formField.setAttribute('class', SHOW_FORM_CLASS);
        var checkbox = document.querySelectorAll(CHECKBOX_SELECTOR);
        for (var i=0; i < checkbox.length; i++) {
            checkbox[i].setAttribute('class', CLEAR_ATTR);
        }
    });
}

function selectRows(event) {
    'use strict';
    event.addEventListener('click', function(event) {
        var item = this.getElementsByTagName('input');
        for (var i=0; i < item.length; i++) {
            if (item[i].checked == true) {
                this.style.backgroundColor = "#FFFFFF";
                item[i].removeAttribute('checked');
            } else {
                item[i].setAttribute('checked', true);
                this.style.backgroundColor = "#A7FFD8";
            }
        }
    });
}

function updateDate(row) {
    'use strict';
    row.addEventListener('click', function (event) {
        console.log('double clicked...');
    });
}

function initializeEvents() {
    var tasks = document.querySelectorAll('.tableSet');
    tasks.forEach(selectRows);
    showMassUpdate();
}

initializeEvents();
