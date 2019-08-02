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

    $('.filter-toggle').click(function () {
        $('.filter').toggle("slow");
    });

    $('.select2').select2({
        placeholder: "Выберите значения"
    });
});