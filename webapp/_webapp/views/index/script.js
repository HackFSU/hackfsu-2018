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
    var scheduleDayContainer = $('#schedule-day-container');
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

        // Add it to correct day
        var date = item.start.format('YYYY-MM-DD');
        var scheduleDay = scheduleDayContainer.find('.schedule-day').filter(function() {
            return $(this).data('date') === date;
        });

        if (scheduleDay.length === 0) {
            scheduleDay = $(
                '<div class="schedule-day">' +
                    '<h1>'+item.start.format('dddd')+'</h1>' +
                    '<div class="schedule-item-container"></div>' +
                '</div>'
            ).appendTo(scheduleDayContainer);
            scheduleDay.data('date', date);
        }
        scheduleDay.find('.schedule-item-container').append(e);
    }


    $.ajaxGet({
        url: '/api/hackathon/get/schedule_items',
        success: function(data) {
            data.schedule_items.forEach(function(item) {
                addScheduleItem(item);
            });
        }
    });



    /**
     * Prizes
     */
    var prizesContainer = $('#prize-container');

    function addPrize(prize) {
        prizesContainer.append(
            '<div class="prize"><div class="row">' +

                '<div class="col-xs-7">' +
                    '<span class="prize-title">'+prize.title+'</span>' +
                    '<span class="fa fa-trophy"></span>' +
                    (prize.description? '<div class="prize-description"><span>'+prize.description+'</span></div>' : '') +
                '</div>' +
                '<div class="col-xs-5 prize-award-giver">' +
                    '<span>'+prize.award_giver+'</span>' +
                '</div>' +
            '</div></div>'
        );
    }


    $.ajaxGet({
        url: '/api/hackathon/get/prizes',
        success: function(data) {
            data.prizes.forEach(function(prize) {
                addPrize(prize);
            });
        }
    });


})();
