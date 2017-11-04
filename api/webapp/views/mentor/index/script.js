/**
 * Mentor help request view page
 */

(function($) {
    'use strict';

    // Setup DataTable
    var tablePending = $('table#requests-pending');
    var tableClaimedUser = $('table#requests-claimed-user');
    var tableClaimedOther = $('table#requests-claimed-other');

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


    function filterData(data, type) {
        var filteredData = [];

        data.forEach(function(row) {
            switch (type) {
                case 'user':
                    if (row.assigned_mentor && row.assigned_mentor.is_me) {
                        filteredData.push(row);
                    }
                    break;
                case 'other':
                    if (row.assigned_mentor && !row.assigned_mentor.is_me) {
                        filteredData.push(row);
                    }
                    break;
                case 'pending':
                default:
                    if (!row.assigned_mentor) {
                        filteredData.push(row);
                    }
            }
        });

        return filteredData;
    }

    // Create page
    createTable(tablePending, COLS);
    createTable(tableClaimedOther, COLS);
    createTable(tableClaimedUser, COLS);
    getData().done(function(requests) {
        populateTable(tablePending, COLS, filterData(requests, 'pending'));
        populateTable(tableClaimedUser, COLS, filterData(requests, 'user'));
        populateTable(tableClaimedOther, COLS, filterData(requests, 'other'));
    });


    // Reload after a minute
    setTimeout(function() {
       window.location.reload(1);
    }, 2*60*1000);


})(jQuery);
