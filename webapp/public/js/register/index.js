import $ from 'jquery';

import { initSections, revealSection } from './sections';
import {
    submitHackerInfo,
    validateUserForm,
    validateAttendeeForm,
    validateHackerForm
} from './submit';

import './resume-upload';

$(document).ready(function() {
    initSections();
});

//
//
//

function displayErrorFromJson (err) {
    var msg = JSON.stringify(err.responseJSON.message);
    msg = msg.replace(/{|}|'|"|\[|\]/g, '');
    msg = msg.replace(/, /g, '\n');
    alert(msg);
}

//
//  Button handlers
//

//Buttons
var btn1 = $('section#part1 button');
var btn2 = $('section#part2 button');
var btn3 = $('section#part3 button');

btn1.on('click', e => {

    validateUserForm();
    revealSection(2);

    $('html, body').animate({
        scrollTop: $('#part2').offset().top
    }, 400, 'swing');
});

btn2.on('click', e => {
    validateAttendeeForm();
    revealSection(3);

    $('html, body').animate({
        scrollTop: $('#part3').offset().top
    }, 400, 'swing');
});

btn3.on('click', () => {


    validateUserForm();
    validateAttendeeForm();
    validateHackerForm();

    btn3.prop('disabled', true);

    submitHackerInfo(
        function success () {
            alert('Okay, you\'re registered!');
        },
        function error (err) {
            btn3.removeAttr('disabled');
            displayErrorFromJson(err);
            console.log(err);
        }
    );
});
