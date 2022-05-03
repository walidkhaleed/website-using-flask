
$(document).ready(function () {
    $('.radio').on('change', function () {
        var val = $(this).attr('data-class');
        $('.allshow').hide();
        $('.' + val).show();
    });
});

$(document).ready(function () {
    $('.single').on('change', function () {
        var val = $(this).attr('data-class');
        $('.allshowp').hide();
        $('.' + val).show();
    });
});




