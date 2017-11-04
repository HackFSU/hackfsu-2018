/**
 * Mentor help request view page
 */

(function($) {
    'use strict';

    var table = $('table#hacks');

    var STATUS_PENDING = 0;
    var STATUS_COMPLETE = 1;
    var STATUS_CANCELED = 2;
    var STATUS_CHOICES = {};
    STATUS_CHOICES[STATUS_PENDING] ='Pending';
    STATUS_CHOICES[STATUS_COMPLETE] = 'Complete';
    STATUS_CHOICES[STATUS_CANCELED] = 'Canceled';


    var COLS = {
        'Table Number': { data: 'hack_table_number' },
        'Hack Name': { data: 'hack_name' },
        'Status': { data: function(row) {
            return STATUS_CHOICES[row.assignment_status];
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
            url: '/api/judge/get/pending_hack_assignments'
        })
            .done(function(res) {
                dfd.resolve(res['hacks']);
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
                [colNames.indexOf('Table Number'), 'asc']
            ],
            select: {
                style: 'single'
            },
            buttons: [
                {
                    extend: 'selected',
                    text: 'Judge Hack',
                    className: 'btn-form btn-form-sm',
                    action: function (e, dt) {
                        var row = dt.rows({selected: true}).data()[0];
                        window.location.href = '/judge/hack/' + row.assignment_id + '/'
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
