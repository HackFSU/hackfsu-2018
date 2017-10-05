/**
 * Mentor help request view page
 */

(function($) {
    'use strict';

    var table = $('table#hacks');

    var COLS = {
        'Table Number': { data: 'table_number' },
        'Hack Name': { data: 'name' },
        'Expo': { data: 'expo' },
        'Opt-In Prizes' : { data: 'criteria'}
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
            url: '/api/judge/get/hacks_with_criteria'
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
                "<'row flex-align-center flex-wrap'<'col-sm-6'l><'col-sm-6'f>>" +
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
            ]
        });
    }

    // Create page
    createTable(table, COLS);
    getData().done(function(data) {
        populateTable(table, COLS, data);
    });


})(jQuery);
