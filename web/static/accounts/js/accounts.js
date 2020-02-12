function modifyAccount() {
    $('#modify-account-modal')
        .modal('show')
}

$('#modify-account-submit').click(function (e) {
    e.preventDefault();
    $('#modify-account-form').submit();
})
