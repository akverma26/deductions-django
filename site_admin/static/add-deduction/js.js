$(document).ready(function(){

    $('#fetch-info').click(function(){
        $.ajax({
            type: 'GET',
            url: '/site-admin/add-deduction/',
            data: {'manifest-url': $('#manifest_url').val(), 'request-type': 'fetch-info'},
            success: function(data){
                $('.input-details').html(data.html);
            }
        });
    });

});