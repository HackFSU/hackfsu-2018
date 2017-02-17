/**
 * Mentor help request view page
 */

(function($) {
    'use strict';

    // Setup DataTable
    var table = $('table#help-requests');
    var COLS = {
        'Name': { data: 'attendee.name' },
        'Request': { data: 'request' },
        'Status': { data: function (row, type) {
            var assignedMentor = row.assigned_mentor;
            if (type === 'display') {
                if (assignedMentor) {
                    if (assignedMentor.is_me) {
                        return 'Claimed by you';
                    }
                    return 'Claimed by ' + assignedMentor.name;
                }
                return 'Waiting for mentor!';
            }

            // Sort by claimed/unclaimed
            return assignedMentor? 1 : 0;
        }},
        'Submitted At': { data: function (row, type) {
            var created = hackUtil.deserializeDateTime(row.created);
            if (type === 'display') {
                // Minimal display
                return created.format('ddd hh:mm a');
            }

            // Exact time for sorting
            return created.valueOf();
        }}

    };

    /**
     * Formats the table html
     */
    function createTable(table, colData) {
        var tableHead = $('<thead><tr></tr></thead>');
        var tableHeadRow = tableHead.find('tr');

        Object.keys(colData).forEach(function(columnName) {
            tableHeadRow.append('<th>'+columnName+'</th>');
        });

        table.append(tableHead);
        table.append('<tbody></tbody>');
    }

    /**
     * Retrieves data
     */
    function getData() {
        var dfd = $.Deferred();

        $.ajaxGet({
            url: '/api/mentor/request/get'
        })
            .done(function(res) {
                dfd.resolve(res['help_requests']);
            })
            .fail(function(err) {
                dfd.reject(err);
            });

        return dfd.promise();
    }

    /**
     * Populates the DataTable with help requests
     */
    function populateTable(table, colData, data) {
        var colNames = Object.keys(colData);

        var dt = table.DataTable({
            dom:
                "<'row flex-align-center flex-wrap'<'col-sm-4'l><'col-sm-4'<'flex-center'B>><'col-sm-4'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-5'i><'col-sm-7'p>>",
            // scrollX: true,
            responsive: true,
            lengthMenu: [[25, 50, 100, -1], [25, 50, 100, 'All']],
            data: data,
            columns: $.map(colData, function(data) {
                return data;
            }),
            order: [
                [colNames.indexOf('Status'), 'asc'],
                [colNames.indexOf('Submitted At'), 'desc']
            ],
            select: {
                style: 'single'
            },
            buttons: [
                {
                    extend: 'selected',
                    text: 'View Full Request',
                    className: 'btn-form btn-form-sm',
                    action: function (e, dt) {
                        var row = dt.rows({selected: true}).data()[0];
                        window.location.href = '/mentor/request/' + row.id;
                    }
                }
            ]
        });

        return dt;
    }


    // Create page
    createTable(table, COLS);
    getData().done(function(requests) {
        console.log(requests);
        populateTable(table, COLS, requests);
    });


    // Reload after a minute
    setTimeout(function() {
       window.location.reload(1);
    }, 60*1000);


})(jQuery);
