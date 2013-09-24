/*jslint browser: true, indent: 4, maxlen: 80 */

/* Clear input `input_name`. */
function clearInput(inputName) {
    'use strict';
    document.querySelector(
        'section#content input[name=' + inputName + ']'
    ).value = '';
}

/* Populate input `input_name` with the current date. */
function fillDate(inputName) {
    'use strict';
    // `toISOString()` returns e.g. "2013-09-24T19:34:17.974Z"
    /*jslint regexp: true */
    // FIXME: date has GMT timezone
    document.querySelector(
        'section#content input[name=' + inputName + ']'
    ).value = new Date().toISOString().replace(/T.*/, '');
}

/* Populate input `input_name` with the current date and time. */
function fillDateTime(inputName) {
    'use strict';
    // `toISOString()` returns e.g. "2013-09-24T19:34:17.974Z"
    /*jslint regexp: true */
    // FIXME: datetime has GMT timezone
    document.querySelector(
        'section#content input[name=' + inputName + ']'
    ).value = new Date().toISOString().
        replace(/T/, ' ').
        replace(/(\d{2}:\d{2}).*/, '$1');
}

/* Check to see if the browser supports date inputs.
 *
 * Create a dummy element that will never be attached to the DOM tree and use it
 * to probe the capabilities of the browser. If the browser does not provide a
 * custom control for date inputs, find all date inputs and fiddle with their
 * attributes.
 *
 * For the definition of a valid date string, see:
 * http://developers.whatwg.org/common-microsyntaxes.html#valid-date-string
 */
function checkDateInputs() {
    'use strict';
    var i, inputs, dummyInput;
    dummyInput = document.createElement('input');
    dummyInput.setAttribute('type', 'date');
    if ('date' !== dummyInput.type) {
        inputs = document.querySelectorAll(
            'section#content input[type="date"]'
        );
        for (i = 0; i < inputs.length; i += 1) {
            inputs[i].type = 'text';
            inputs[i].placeholder = 'yyyy-mm-dd';
        }
    }
}

/* Check to see if the browser supports datetime inputs.
 *
 * Create a dummy element that will never be attached to the DOM tree and use it
 * to probe the capabilities of the browser. If the browser does not provide a
 * custom control for datetime inputs, find all datetime inputs and fiddle with
 * their attributes.
 *
 * For the definition of a valid datetime string, see:
 * http://developers.whatwg.org/common-microsyntaxes.html#local-dates-and-times
 */
function checkDateTimeInputs() {
    'use strict';
    var i, inputs, dummyInput;
    dummyInput = document.createElement('input');
    dummyInput.setAttribute('type', 'datetime');
    if ('datetime' !== dummyInput.type) {
        inputs = document.querySelectorAll(
            'section#content input[type="datetime"]'
        );
        for (i = 0; i < inputs.length; i += 1) {
            inputs[i].type = 'text';
            inputs[i].placeholder = 'yyyy-mm-dd hh:mm';
        }
    }
}

// Fire events as soon as the DOM is loaded. (do not use `window.onload`)
if (document.addEventListener) {
    document.addEventListener('DOMContentLoaded', checkDateInputs, false);
    document.addEventListener('DOMContentLoaded', checkDateTimeInputs, false);
}
