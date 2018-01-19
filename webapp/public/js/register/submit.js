import $ from 'jquery';
import empty from 'is-empty';

//
//  Fetch and clean data
//

function getUserInfo () {
    const userForm = $('form#userForm');

    const emailInput           = userForm.find('input[name="email"]');
    const passwordInput        = userForm.find('input[name="password"]');
    const passwordConfirmInput = userForm.find('input[name="confirmPassword"]');

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
    const attendeeForm = $('form#attendeeForm');

    const firstNameInput     = attendeeForm.find('input[name="firstName"]');
    const lastNameInput      = attendeeForm.find('input[name="lastName"]');
    const phoneNumberInput   = attendeeForm.find('input[name="phoneNumber"]');
    const githubInput        = attendeeForm.find('input[name="github"]');
    const linkedinInput      = attendeeForm.find('input[name="linkedin"]');
    const shirtSizeSelect    = attendeeForm.find('select[name="shirtSize"]');
    const commentsInput      = attendeeForm.find('input[name="comments"]');
    const codeOfConductCheck = attendeeForm.find('input[name="codeOfConduct"]');
    const termsAndCondCheck  = attendeeForm.find('input[name="termsAndConditions"]');

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

function validateAttendeeForm() {

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

function submitAttendeeInfo (success) {

    validateUserForm();
    validateAttendeeForm();

    let userInfo = getUserInfo();
    let attedeeInfo = getAttendeeInfo();
    let data = Object.assign(userInfo, attedeeInfo);

    $.ajax({
        url: process.env.API_HOST + '/api/user/register',
        method: 'POST',
        data: data,
        crossDomain: true,
        beforeSend: function () {
            console.log('sending!');
        },
        success: success,
        error: (e) => {
            var msg = JSON.stringify(e.responseJSON.message);
            msg = msg.replace(/{|}|'|"|\[|\]/g, '');
            msg = msg.replace(/, /g, '\n');
            alert(msg);
        }
    });
}


export {
    validateUserForm,
    submitAttendeeInfo
};
