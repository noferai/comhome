$(document).ready(function () {
    let word = window.location.pathname.split('/')[1];
    $('#navbarNav a.nav-link').each(function () {
        if (word === "") {
            $("#home").addClass('active');
        } else if ($(this).prop('href').includes(word) && word) {
            $(this).addClass('active');
        }
    });

    $(".date input").attr("type", "date");

    $('.select2').select2({
        placeholder: "Выберите значения"
    });

    $("#table-search").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("table.table > tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

});