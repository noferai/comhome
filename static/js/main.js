$(document).ready(function () {
    word = window.location.pathname.split('/')[1];
    $('#navbarNav a.nav-link').each(function(){
        if(word === ""){
            $("#home").addClass('active');
        }
        else if ($(this).prop('href').includes(word) && word) {
            $(this).addClass('active');
        }
    });
    $(".date input").attr("type", "date");
    console.log("loh-global");
});