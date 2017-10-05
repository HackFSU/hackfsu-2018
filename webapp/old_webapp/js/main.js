/**
 * Main global JavaScript for all pages
 */


(function() {
    'use strict';

    var hackUtil = window.hackUtil = {};

    hackUtil.SCHEDULE_ITEM_TYPES = {
        0: 'Key',
        1: 'Tech Talk',
        2: 'Food',
        3: 'Social',
        4: 'Miscellaneous'
    };

    hackUtil.GROUP = {
        user: 'user',
        attendee: 'attendee',
        hacker: 'hacker',
        judge: 'judge',
        mentor: 'mentor',
        organizer: 'organizer',
        pending_hacker: 'pending-hacker',
        pending_judge: 'pending-judge',
        pending_mentor: 'pending-mentor',
        pending_organizer: 'pending-organizer',
        admin: 'admin'
    };

    hackUtil.getNiceGroupList = function(prefix, groups) {
        groups = [].concat(groups);

        // Remove 'attendee' from list.
        var i = groups.indexOf(hackUtil.GROUP.attendee);
        if (i !== -1) {
            groups.splice(i, 1);
        }

        // Empty group lists will just be users
        if (groups.length === 0) {
            groups.push('regular ' + hackUtil.GROUP.user);
        }

        var groupString = prefix + ' a ' + groups.sort().join(' and a ');
        groupString = groupString.replace(/-/g, ' ').replace(/(a)\s([aeio])/g, 'an $2') + '.';

        return groupString;
    };

    /**
     * Date time handling
     * https://docs.python.org/2/library/datetime.html#datetime.datetime.isoformat -> momentjs format
     */

    hackUtil.PYTHON_DATETIME_SERIALIZED_ISO_FORMAT = 'YYYY-MM-DDTHH:mm:ss:SSSSSSSSSZ';

    hackUtil.deserializeDateTime = function(pythonIsoDateString) {
        return moment.utc(pythonIsoDateString, hackUtil.PYTHON_DATETIME_SERIALIZED_ISO_FORMAT).local();
    };

    hackUtil.jsonToFormData = function(jsonData) {
        var fd = new FormData();
        for (var key in jsonData) {
            if (jsonData.hasOwnProperty(key) && jsonData[key] !== null && jsonData[key] !== undefined) {
                fd.append(key, jsonData[key]);
            }
        }
        return fd;
    };

    hackUtil.ajaxJsonSubmit = function(options) {
        var dfd = $.Deferred();
        var defaultAjaxOptions = {
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            success: function(response) {
                if (response.error) {
                    console.error('Server Error:', response.error);
                    dfd.reject(response.error);
                } else {
                    dfd.resolve(response);
                }
            },
            error: function(response) {
                console.error('Server Error:', response);
                var err = JSON.parse(response.responseText);
                alert(err.cause + ': ' + err.message);
                dfd.reject(response);
            }
        };

        $.ajax($.extend({}, defaultAjaxOptions, options));

        return dfd.promise();
    };



})();
