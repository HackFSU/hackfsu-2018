/**
 * Mentor help request view page
 */

(function($) {
    'use strict';

    var table = $('table#judges');
    var form = $('form#settings');

    var COLS = {
        'Name': { data: 'name' },
        'Pending Assignments': { data: 'assignments_pending' },
        'Completed Assignments': { data: 'assignments_completed' },
        'Canceled Assignments': { data: 'assignments_canceled' }
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
            url: '/api/judge/get/approved_and_checked_in'
        })
            .done(function(res) {
                dfd.resolve(res['judges']);
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

        table.DataTable({
            dom:
                "<'row flex-align-center flex-wrap'<'col-sm-4'l><'col-sm-4'<'flex-center'B>><'col-sm-4'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-5'i><'col-sm-7'p>>",
            responsive: true,
            lengthMenu: [[25, 50, 100, -1], [25, 50, 100, 'All']],
            data: data,
            columns: $.map(colData, function(data) {
                return data;
            }),
            order: [
                [colNames.indexOf('Name'), 'asc']
            ],
            select: {
                style: 'single'
            },
            buttons: [
                {
                    extend: 'selected',
                    text: 'Assign Hacks',
                    className: 'btn-form btn-form-sm',
                    action: function (e, dt) {
                        var row = dt.rows({selected: true}).data()[0];
                        hackUtil.ajaxJsonSubmit({
                            url: '/api/judge/assign_hacks',
                            data: JSON.stringify({
                                max_hacks: form.find('input[name="max_hacks"]').val(),
                                max_judge_count: form.find('input[name="max_judge_count"]').val(),
                                judge_info_id: row.id
                            })
                        }).done(function(res) {
                            alert('Assigned ' + res.new_assignments  + ' new hacks to ' + row.name);
                            window.location.reload(1);
                        });
                    }
                }
            ]
        });
    }

    // Create page
    createTable(table, COLS);
    getData().done(function(data) {
        populateTable(table, COLS, data);
    });


})(jQuery);
