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
                var logs = '';
                for(var log of data.logs) {
                    if(log[0]=='e'){
                        logs+='<div style="color: rgb(255,0,0);">Error: '+log[1]+'</div>';
                    }
                    else if(log[0]=='s'){
                        logs+='<div style="color: rgb(0,255,0);">Success: '+log[1]+'</div>';
                    }
                    else if(log[0]=='w') {
                        logs+='<div style="color: rgb(0,0,255);">Warning: '+log[1]+'</div>';
                    }
                    else {
                        logs+='<div style="color: rgb(255,255,255);">Message: '+log[1]+'</div>';
                    }
                }
                $('#logs').html(logs);
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

            var delete_keys = []

            if( data.fetched_files_html ){
                $('.input-details').html(data.fetched_files_html);
                delete_keys.push('fetched_files_html');
            }

            if(data.refresh_downloading) {
                for( var el in data.refresh_downloading ) {
                    if(data.refresh_downloading[el]=='Failed') {
                        $('#'+el).parent().find('td').css({'background': 'rgba(255,0,0,0.3)'});
                        $('#'+el).html(data.refresh_downloading[el]);
                    }
                    else {
                        $('#'+el).html(data.refresh_downloading[el]);
                    }
                }
                delete_keys.push('refresh_downloading');
            }

            if(data.finish) {
                return;
            }

            setTimeout(function(){
                trackServer(delete_keys);
            }, 1000);
        }
    });
}