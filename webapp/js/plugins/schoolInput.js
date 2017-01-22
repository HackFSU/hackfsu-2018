/**
 * Makes a regular input autocomplete with school names
 */

(function($) {
    'use strict';

    var schoolData = null;
    function getSchoolData() {
        var dfd = $.Deferred();
        if (schoolData !== null) {
            return dfd.resolve(schoolData);
        }

        schoolData = [];

        // Get it
        $.get({
            url: '/api/school/get',
            headers: {
                'HTTP_X_CSRFTOKEN': Cookies.get('csrftoken')
            },
            success: function(res) {
                schoolData = res.school_choices;
                dfd.resolve(schoolData);
            },
            fail: function(err) {
                console.error(err);
                dfd.resolve([]);
            }
        });

        return dfd;
    }

    function getOptionsFromData(data) {
        var options = [];
        data.forEach(function(school) {
            options.push({
                value: school.name,
                data: school.id
            });
        });
        return options;
    }

    function getIdFromName(data, name) {
        var id = '';
        data.forEach(function(school) {
            if (school.name === name) {
                id = school.id;
                return false;
            }
        });
        return id;
    }

    $.fn.schoolInput = function(task, arg) {
        var self = $(this);
        getSchoolData().then(function(data) {
            if (task === 'getData') {
                return data;
            } else if (task === 'getId') {
                return getIdFromName(data, arg);
            }

            // Setup autocomplete
            self.autocomplete({
                lookup: getOptionsFromData(data),
                onSelect: function(option) {
                    self.val(option.value);
                }
            });
        });
    };

})(jQuery);
