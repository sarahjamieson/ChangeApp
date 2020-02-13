$(document).ready(function() {
    $('#user-history-table').DataTable({
        order: [[1, 'desc']],
        lengthMenu: [[5]],
        bLengthChange: false,
        bFilter: false,
        bInfo: false,
        columnDefs: [
            {
                targets: [1],
                visible: false,
                searchable: false,
            },
        ],
    });
});

function modifyAccount() {
    $('#modify-account-modal')
        .modal('show')
}

$('#modify-account-submit').click(function (e) {
    e.preventDefault();
    $('#modify-account-form').submit();
})

