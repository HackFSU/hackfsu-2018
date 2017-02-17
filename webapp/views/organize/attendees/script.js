/**
 * Mentor help request view page
 */

(function($) {
    'use strict';

    // Setup DataTable
    var table = $('table#attendees');
    var COLS = {
        'Name': { data: 'name'},
        'Email': { data: 'email' },
        'Checked In': { data: 'checked_in' },
        'Approved As': { data: function (row, type) {
            if (row.groups) {
                return row.groups.join(', ');
            }
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
     * Populates the DataTable with help requests
     */
    function populateTable(table, colData) {
        var colNames = Object.keys(colData);

        table.DataTable({
            dom:
                "<'row flex-align-center flex-wrap'<'col-sm-4'l><'col-sm-4'<'flex-center'B>><'col-sm-4'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-5'i><'col-sm-7'p>>",
            responsive: true,
            lengthMenu: [[10, 25, 50], [10, 25, 50]],
            serverSide: true,
            processing: true,
            searchDelay: 1000,
            ajax: '/api/attendee/get/approved_full',
            columns: $.map(colData, function(data) {
                return data;
            }),
            ordering: false,
            select: {
                style: 'single'
            },
            buttons: [
                {
                    extend: 'selected',
                    text: 'Check in',
                    className: 'btn-form btn-form-sm',
                    action: function (e, dt) {
                        var row = dt.rows({selected: true}).data()[0];
                        hackUtil.ajaxJsonSubmit({
                            'url': '/api/attendee/check_in',
                            data: JSON.stringify({
                                attendee_status_id: row.id
                            })
                        }).done(function () {
                            alert(row.name + ' has been checked in');
                            dt.ajax.reload();
                        });
                    }
                },
                // {
                //     extend: 'selected',
                //     text: 'Give Wifi',
                //     className: 'btn-form btn-form-sm',
                //     action: function (e, dt) {
                //         var row = dt.rows({selected: true}).data()[0];
                //         alert('TODO');
                //     }
                // }
            ]
        });
    }


    // Create page
    createTable(table, COLS);
    populateTable(table, COLS);


})(jQuery);
