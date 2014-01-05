/*jslint browser: true, indent: 4, maxlen: 80 */

/* Pad `string` with leading zeroes until it is `length` characters long. */
function padString(string, length) {
    'use strict';
    if (string.length >= length) {
        return string;
    }
    return padString('0' + string, length);
}

/* Return a string `length` characters long, padded with leading zeroes. */
function padNumber(number, length) {
    'use strict';
    return padString(number.toString(), length);
}

/* Return a string in the format yyyy-mm-dd. Respect `date`'s time zone. */
function yearMonthDate(date) {
    'use strict';
    return [
        date.getFullYear(),
        padNumber(date.getMonth() + 1, 2),
        padNumber(date.getDate(), 2)
    ].join('-');
}

/* Return a string in the format hh:mm. Respect `date`'s time zone. */
function hourMinute(date) {
    'use strict';
    return [
        padNumber(date.getHours(), 2),
        padNumber(date.getMinutes(), 2)
    ].join(':');
}

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
    document.querySelector(
        'section#content input[name=' + inputName + ']'
    ).value = yearMonthDate(new Date());
}

/* Populate input `input_name` with the current date and time. */
function fillDateTime(inputName) {
    'use strict';
    var now = new Date();
    document.querySelector(
        'section#content input[name=' + inputName + ']'
    ).value = yearMonthDate(now) + ' ' + hourMinute(now);
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
