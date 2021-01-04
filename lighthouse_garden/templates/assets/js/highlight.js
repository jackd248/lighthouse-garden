$(function () {
    highlightRow();
    $('.share-link').click(function() {
        setTimeout(function(){ highlightRow(); }, 200);

    });

    function highlightRow() {
        const anchor = window.location.hash.substr(1);
            $('tr').removeClass('highlight');
        if (anchor !== '') {
            $('#' + anchor).addClass('highlight');
        }
    }
})