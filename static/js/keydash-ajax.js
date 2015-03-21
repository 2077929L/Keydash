$(document).ready(function() {

    $('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/keydash/suggest_friends/', {suggestion: query}, function(data){
            $('#cats').html(data);
        });
    });

});