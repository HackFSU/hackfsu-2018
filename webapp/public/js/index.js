$(document).ready(function() {
  $('select').material_select();
});


function landingPageInit() {
    if(window.location.pathname === '/') {
      console.log('working');
      var confetti = $('.confetti');
      for(var i = 0; i < 100; i++) {
        confetti.clone().appendTo(".conf-cont");
      }
      $('#submit-button').bind("click", function() {
      const url = "https://2017.hackfsu.com/api/preview/register";
      var email = $('#email').get(0).value;
      var interest = $('#interest').get(0).value;
      function validateEmail(email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
      }

      if(!email || !validateEmail(email)) {
        alert("Please enter a valid email.");
      } else if(!interest) {
        alert("Please indicate your preference.");
      } else {
        $.post(url, {
          email: email,
          interest: interest
        });

          $('#submit-button img').toggle()
          $('#submit-button').append("<span>Submitted!</span>");
          $('#submit-button').unbind("click");
      }
    })
  }
};



function registerPageInit() {
  if(window.location.pathname === '/register') {
    console.log('something')
    $('#submit-button').bind("click", function() {
      console.log('something')
      const url = "https://2017.hackfsu.com/api/preview/register";
      var interest = $('#interest').get(0).value;
      var email = $('#email').get(0).value;
      var password = $('#email').get(0).value;
      var confirmPassword = $('#confirmPassword').get(0).value;
      var firstName = $('#firstName').get(0).value;
      var lastName = $('#lastName').get(0).value;
      var phoneNumber = $('#phoneNumber').get(0).value;
      var shirtSize = $('#shirtSize').get(0).value;
      var github = $('#github').get(0).value;
      var dietaryRestrictions = {
        vegetarian: $('#vegetarian').get(0).value,
        vegan: $('#vegan').get(0).value,
        allergies: $('#allergies').get(0).value,
        other: $('#other').get(0).value
      };
      var codeOfConduct = $('codeOfConduct').get(0).value;
      var school = $('#school').get(0).value;
      var status = $('#status').get(0).value;
      var major = $('#major').get(0).value;
      var firstHackathon = $('#firstHackathon').get(0).value;
      var ageRadio = $('#ageRadio').get(0).value;
      var hackingInterests = {
        frontEnd: $('#frontEnd').get(0).value,
        backEnd: $('#backEnd').get(0).value,
        web: $('#web').get(0).value,
        hardware: $('#hardware').get(0).value,
        ios: $('#ios').get(0).value,
        android: $('#android').get(0).value,
        virtualReality: $('#virtualReality').get(0).value,
        design: $('#design').get(0).value
      };




      if(validated()) {
        $.post(url, {
          interest: interest,
          email: email,
          password: password,
          confirmPassword: confirmPassword,
          firstName: firstName,
          lastName: lastName,
          phoneNumber: phoneNumber,
          shirtSize: shirtSize,
          github: github,
          linkedin: linkedin,
          dietaryRestrictions: dietaryRestrictions,
          codeOfConduct: codeOfConduct,
          school: school,
          status: status,
          major: major,
          firstHackathon: firstHackathon,
          ageRadio: ageRadio,
          hackingInterests: hackingInterests
        });

        // $('#submit-button p').toggle()
        $('#submit-button').append("<span>Submitted!</span>");
        $('#submit-button').unbind("click");
      }


      function validated() {
        console.log('something')
        var validated = false;

        if(!interest){
          alert("Please indicate your preference.");
        } else if(!email || !validateEmail()) {
          alert("Please enter a valid email.");
        } else if(!password) {
          alert("Please enter a valid password.");
        } else if(!confirmPassword || validateConfirmPassword()) {
          alert("Please confirm your password exactly.");
        } else if(!firstName) {
          alert("Please enter your first name.");
        } else if(!lastName) {
          alert("Please enter your last name.");
        } else if(!phoneNumber) {
          alert("Please enter your phone number.");
        } else if(!shirtSize) {
          alert("Please select a shirt size.");
        } else {
          validated = true;
        }
        
        return validated;

        function validateEmail(email) {
          var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return re.test(email);
        }

        function validateConfirmPassword() {
          return password === confirmPassword
        }
      };
    })
  }
};



landingPageInit();
registerPageInit();
