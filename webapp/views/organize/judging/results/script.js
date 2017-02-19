/**
 * Mentor help request view page
 */

(function($) {
    'use strict';

    var CRITERIA_TYPE_OVERALL = 0;
    var CRITERIA_TYPE_SUPERLATIVE = 1;

    var table = $('table#hacks');

    var COLS = {
        'Table Number': { data: 'table_number' },
        'Hack Name': { data: 'name' }
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
            url: '/api/judge/get/grades'
        })
            .done(function(data) {
                dfd.resolve(data);
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

    console.log('Loading');
    // Create page
    getData().done(function(data) {
        var crits = data['criteria_names'];
        var hack_rows = [];
        console.log(data);
        // Create columns with order;
        var crit_id_order = [];
        var OVERALL_ID = 100;
        COLS['Overall Score'] = { data: function(row) {
            if (row[OVERALL_ID]) {
                return row[OVERALL_ID]
            } else {
                return 'N/A'
            }
        }};

        Object.keys(crits[CRITERIA_TYPE_OVERALL]).forEach(function(critId) {
            crit_id_order += critId;
            COLS[crits[CRITERIA_TYPE_OVERALL][critId]] = { data: function(row) {
                if (row[critId]) {
                    return row[critId]
                } else {
                    return 'N/A'
                }
            }};
        });
        Object.keys(crits[CRITERIA_TYPE_SUPERLATIVE]).forEach(function(critId) {
            crit_id_order += critId;
            COLS[crits[CRITERIA_TYPE_SUPERLATIVE][critId]] = { data: function(row) {
                if (row[critId]) {
                    return row[critId]
                } else {
                    return 'N/A'
                }
            }};
        });

        // Summarize data
        data['graded_hacks'].forEach(function(hack_result) {
            var results = hack_result.results;
            var hData = {
                name: hack_result.hack.name,
                table_number: hack_result.hack.table_number
            };

            Object.keys(results[CRITERIA_TYPE_OVERALL]).forEach(function(critId) {
                var result = results[CRITERIA_TYPE_OVERALL][critId];
                hData[critId] = result['contribution'] + ' of ' + result['times_graded'];
            });
            Object.keys(results[CRITERIA_TYPE_SUPERLATIVE]).forEach(function(critId) {
                var result = results[CRITERIA_TYPE_SUPERLATIVE][critId];
                hData[critId] = result['contribution'] + ' of ' + result['times_graded'];
            });

            hack_rows.push(hData);
        });

        // Convert dict to ordered rows
        createTable(table, COLS);
        populateTable(table, COLS, hack_rows);
    });


})(jQuery);
