import $ from 'jquery';
import empty from 'is-empty';

//
//  Fetch and clean data
//

function getUserInfo () {
    const form = $('form.registerForm');

    const emailInput           = form.find('input[name="email"]');
    const passwordInput        = form.find('input[name="password"]');
    const passwordConfirmInput = form.find('input[name="confirmPassword"]');

    let email = emailInput.val().trim(),
        password = passwordInput.val().trim(),
        passConfirm = passwordConfirmInput.val().trim();

    return {
        email,
        password,
        passConfirm
    };
}

function getAttendeeInfo () {
    const form = $('form.registerForm');

    const firstNameInput     = form.find('input[name="firstName"]');
    const lastNameInput      = form.find('input[name="lastName"]');
    const phoneNumberInput   = form.find('input[name="phoneNumber"]');
    const githubInput        = form.find('input[name="github"]');
    const linkedinInput      = form.find('input[name="linkedin"]');
    const shirtSizeSelect    = form.find('select[name="shirtSize"]');
    const commentsInput      = form.find('input[name="comments"]');
    const codeOfConductCheck = form.find('input[name="codeOfConduct"]');
    const termsAndCondCheck  = form.find('input[name="termsAndConditions"]');

    let first_name = firstNameInput.val().trim(),
        last_name = lastNameInput.val().trim(),
        phone_number = phoneNumberInput.val().trim().replace(/\D/g,''),
        github = githubInput.val().trim(),
        linkedin = linkedinInput.val().trim(),
        shirt_size = shirtSizeSelect.val().trim(),
        comments = commentsInput.val().trim();

    function getDiet() {
        let diets = [];
        $('#diets input:checked').each(function () {
            diets.push($(this)[0].name);
        });
        return '' + diets.join('; ');
    }

    let diet = getDiet();
    let agree_to_mlh_coc = codeOfConductCheck.is(':checked');
    let agree_to_mlh_data_sharing = termsAndCondCheck.is(':checked');

    return {
        first_name,
        last_name,
        phone_number,
        github,
        linkedin,
        shirt_size,
        diet,
        comments,
        agree_to_mlh_coc,
        agree_to_mlh_data_sharing
    };

}

function getHackerInfo () {
    const form = $('form.registerForm');

    const studentTypeSelect     = form.find('select[name="studentType"]');
    const schoolInput           = form.find('input[name="school"]');
    const majorInput            = form.find('input[name="major"]');
    const firstHackathonBox     = form.find('input[name="firstHackathonYes"]');
    const adultRadioBox         = form.find('input[name="ageRadioYes"]');
    const resumeField           = form.find('input[name="resume"]');

    let school_year             = studentTypeSelect.val().trim(),
        is_first_hackathon      = firstHackathonBox.is(':checked'),
        is_adult                = adultRadioBox.is(':checked'),
        school_major            = majorInput.val().trim(),
        resume                  = resumeField[0].files[0],
        g_recaptcha_response    = grecaptcha.getResponse();


    let is_high_school = school_year === 'HS';
    let new_school_name = schoolInput.val().trim();
    //, school_id;

    return {
        school_year,
        is_high_school,
        is_first_hackathon,
        is_adult,
        school_major,
        resume,
        new_school_name,
        g_recaptcha_response
    };
}

//
//  Validate and submit
//

function validateUserForm () {
    let { email, password, passConfirm } = getUserInfo();

    // TODO further validate email?
    if (empty(email)) {
        let msg = 'Please enter a valid email';
        alert(msg);
        throw new Error(msg);
    }

    if (empty(password)) {
        let msg = 'Password must not be empty';
        alert(msg);
        throw new Error(msg);
    }

    if (password != passConfirm) {
        let msg = 'Passwords do not match';
        alert(msg);
        throw new Error(msg);
    }
}

function validateAttendeeForm () {

    let {
        first_name,
        last_name,
        phone_number,
        agree_to_mlh_coc,
        agree_to_mlh_data_sharing
    } = getAttendeeInfo();

    if (empty(first_name) || empty(last_name) || empty(phone_number)) {
        let msg = 'Please complete all required fields.';
        alert(msg);
        throw new Error(msg);
    }

    if (!agree_to_mlh_coc || !agree_to_mlh_data_sharing) {
        let msg = 'Please agree to all MLH policies.';
        alert(msg);
        throw new Error(msg);
    }

}

function validateHackerForm () {

    let {
        school_year,
        school_major,
        new_school_name,
        g_recaptcha_response
    } = getHackerInfo();

    if (empty(school_year) || empty(school_major) || empty(new_school_name)) {
        let msg = 'Please complete all required fields.';
        alert(msg);
        throw new Error(msg);
    }

    if (!g_recaptcha_response) {
        let msg = 'Please complete the recaptcha';
        alert(msg);
        throw new Error(msg);
    }

}

function getHackerData () {
    let userInfo = getUserInfo();
    let attendeeInfo = getAttendeeInfo();
    let hackerInfo = getHackerInfo();
    return Object.assign({}, userInfo, attendeeInfo, hackerInfo);
}

function submitHackerInfo (before, success, failure) {

    let data = new FormData();

    Object.entries(getHackerData()).forEach(([key, value]) => {
        data.append(key, value);
    });

    $.ajax({
        url: '/register',
        method: 'POST',
        type: 'POST',
        data: data,
        // crossDomain: true,
        beforeSend: before,
        success: success,
        error: failure,
        processData: false,
        contentType: false
    });
}


export {
    validateUserForm,
    validateAttendeeForm,
    validateHackerForm,
    submitHackerInfo,
    getHackerData
};


// $.ajax({
//     url: process.env.API_HOST + '/api/hacker/register',
//     method: 'POST',
//     data: data,
//     crossDomain: true,
//     beforeSend: function () {
//         console.log('sending!');
//     },
//     success: success,
//     error: failure,
//     // processData: false,
//     // contentType: false
// });
