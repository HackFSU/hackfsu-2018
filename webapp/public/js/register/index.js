import $ from 'jquery';

import { initSections, revealSection } from './sections';
import { submitAttendeeInfo, validateUserForm } from './submit';
import './resume-upload';

$(document).ready(function() {
    initSections();
});


//
//  Button handlers
//

//Buttons
var btn1 = $('section#part1 button');
var btn2 = $('section#part2 button');
var btn3 = $('section#part3 button');

btn1.on('click', e => {

    validateUserForm();


    // Do AJAX req to api
    revealSection(2);

    $('html, body').animate({
        scrollTop: $('#part2').offset().top
    }, 500, 'linear');

});

btn2.on('click', e => {
    submitAttendeeInfo(() => {
        revealSection(3);
    });
});
