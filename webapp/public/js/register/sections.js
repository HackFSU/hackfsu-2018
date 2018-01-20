import $ from 'jquery';

//
//  Identify components
//

// Sections
const stage1 = $('section#part1');
const stage2 = $('section#part2');
const stage3 = $('section#part3');
const stages = [stage1, stage2, stage3];

//
//  Set page state
//

const setInitPageState = function (state, animate) {
    // Make sure it's either 1, 2, or 3;
    state = state || 1;
    if (!(1 <= state && state <= 3)) state = 1;

    stages.map(stage => stage.hide(animate || false));

    // stages[state - 1].show(animate || false);
    if (state == 1) stage1.show();
    if (state == 2) stage1.show() && stage2.show();
    if (state == 3) stage3.show();
};

const revealSection = function (stage) {
    // This function is specifically for buttons
    stages[stage - 1].show();
}

const getUrlParameter = function (sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

const initSections = function () {
    setInitPageState(getUrlParameter('stage'));
};

$(document).ready(function() {
    initSections();
});

export {
    initSections,
    revealSection
};

//
//  Button handlers
//

// Buttons
// var btn1 = $('section#part1 button');
// var btn2 = $('section#part2 button');
// var btn3 = $('section#part3 button');

// btn1.on('click', (event) => {

//     // Do AJAX req to api
//     revealSection(2);

//     $('html, body').animate({
//         scrollTop: $('#part2').offset().top
//     }, 500, 'linear');

// });
