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

    $('#refresh-data').click(function(){
        $(this).css('visibility', 'hidden');
        $('#sure').show();
    });

    $('#sure').click(function(){
        $.ajax({
            type: 'GET',
            url: '/site-admin/refresh-files/',
            success: function(data){
                $('.input-details').html(data.html);
            }
        });

        trackServer();
    });

});

function trackServer(delete_keys=[]) {
    $.ajax({
        type: 'GET',
        url: '/site-admin/track-server/',
        data: {'delete-keys': delete_keys},
        success: function(data){

            if( data.fetched_files_html ){
                $('.input-details').html(data.fetched_files_html);
                
                setTimeout(
                    function(){
                        trackServer(['fetched_files_html']);
                    }, 1000
                );
            }

            if(data.refresh_downloading) {
                for( var el in data.refresh_downloading ) {
                    $('#'+el).html(data.refresh_downloading['el']);
                    console.log(el, data.refresh_downloading['el'])
                }
            }

            if(data.finish) {}
            else {
                setTimeout(
                    function(){
                        trackServer();
                    }, 1000
                );

            }
        }
    });
}