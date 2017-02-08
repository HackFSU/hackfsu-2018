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

    /**
     * Date time handling
     * https://docs.python.org/2/library/datetime.html#datetime.datetime.isoformat -> momentjs format
     */

    hackUtil.PYTHON_DATETIME_SERIALIZED_ISO_FORMAT = 'YYYY-MM-DDTHH:mm:ss:SSSSSSSSSZ';

    hackUtil.deserializeDateTime = function(pythonIsoDateString) {
        return moment.utc(pythonIsoDateString, hackUtil.PYTHON_DATETIME_SERIALIZED_ISO_FORMAT).local();
    };

})();
