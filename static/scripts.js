$(window).on('resize', function(){
    var win = $(this); //this = window
    if (win.width() >= 768) {

        $(".container-fluid").addClass("row")
    } else if (win.width() <= 767) {
        $(".container-fluid").removeClass("row")
    }
});