(function() {
    'use strict';

    /**
     * FAQ Text Toggling
     */
    var faqs = $('.faq-item-box');
    var activeClass = 'active';
    faqs.on('click', function() {
        faqs.filter('.' + activeClass).not(this).removeClass(activeClass);
        $(this).toggleClass(activeClass);
    });

    $('#content-container').parallaxIt();




    /**
     * Schedule
     */

    var friSchedule = $('#friSchedule');
    var satSchedule = $('#satSchedule');
    var sunSchedule = $('#sunSchedule');
    var timeFormat = 'h:mma';

    function getScheduleItemIconClass(type) {
        // Return the font-awesome icon
        switch (type) {
            case 0: return 'key';
            case 1: return 'code';
            case 2: return 'cutlery';
            case 3: return 'users';
            default: return 'calendar-o';
        }
    }

    function getScheduleItemTime(item) {
        var str = item.start.format(timeFormat);

        if (item.end) {
            str = str.replace(/(am)|(pm)/g, '');
            str += '-' + item.end.format(timeFormat);
        }

        return str.replace(/:00/g, '');
    }


    function addScheduleItem(item) {
        item.start = hackUtil.deserializeDateTime(item.start);
        if (item.end) {
            item.end = hackUtil.deserializeDateTime(item.end);
        }
        var iconClass = getScheduleItemIconClass(item.type);
        var e = $(
            '<div class="schedule-item"><div class="row">' +
                '<div class="col-xs-8">' +
                    '<span class="schedule-item-name">'+item.name+'</span>' +
                    '<span class="fa fa-'+iconClass+'"></span>' +
                    (item.description? '<div class="schedule-item-description"><span>'+item.description+'</span></div>' : '') +
                '</div>' +
                '<div class="col-xs-4 schedule-item-time">' +
                    '<span>'+getScheduleItemTime(item)+'</span>' +
                '</div>' +
            '</div></div>'
        );

        switch (item.start.format('ddd')) {
            case 'Fri': friSchedule.append(e); break;
            case 'Sat': satSchedule.append(e); break;
            case 'Sun': sunSchedule.append(e); break;
            default:
                console.error('Invalid schedule item start date', item);
        }
    }

    $.ajaxGet({
        url: '/api/hackathon/get/schedule_items',
        success: function(data) {
            data.schedule_items.forEach(function(item) {
                addScheduleItem(item);
            });
        }
    });

})();
