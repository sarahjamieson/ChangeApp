$(document).ready(function() {
    $('#user-history-table').DataTable({
        dom: 'itp',
        order: [[1, 'desc']],
        lengthMenu: [[5]],
        pagingType: 'full',
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
        language: {
            paginate:{
                sNext: '<i class="angle right icon"></i>',
                sLast: '<i class="angle double right icon"></i>',
                sFirst: '<i class="angle double left icon"></i>',
                sPrevious: '<i class="angle left icon"></i>',
            }
        }
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

