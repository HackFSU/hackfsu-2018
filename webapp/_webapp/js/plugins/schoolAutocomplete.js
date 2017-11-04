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
                'X-CSRFToken': Cookies.get('csrftoken')
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
        name = name.toLowerCase().trim();
        $.each(data, function(i, school) {
            if (school.name.toLowerCase().trim() === name) {
                id = school.id;
                return false;
            }
        });
        return id;
    }

    $.fn.schoolAutocomplete = function(task, arg) {
        var self = $(this);

        if (task === 'getId') {
            return getIdFromName(self.data('options'), arg);
        }

        getSchoolData().then(function(data) {
            self.data('options', data);

            // Setup autocomplete
            self.autocomplete({
                lookup: getOptionsFromData(data),
                onSelect: function(option) {
                    self.val(option.value);
                    self.data('option-value', option.data);
                }
            });
        });
    };

})(jQuery);
