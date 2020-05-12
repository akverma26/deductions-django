$(document).ready(function(){

    $('.step-title').click(function(){

        if($(this).parent().parent().find('.step-description-div').first().css('max-height')=='0px'){

            var height = parseInt($(this).parent().parent()[0].scrollHeight);
            $(this).parent().parent().find('.step-description-div').first().css({'max-height': (height+40)+'px'});
            
            var ele = $(this).parent().parent().find('.step-description-div').first();
            setTimeout(function(){
                ele.css({'max-height': 'unset'});
            }, 500);
        }
        else{

            $(this).parent().parent().find('.step-description-div').first().css({'max-height': '0px'});
        }
    });

    $('.code-info-button-div').click(function(){

        if($(this).parent().parent().find('.code-description-div').first().css('max-height')=='0px'){

            var height = parseInt($(this).parent().parent()[0].scrollHeight);
            $(this).parent().parent().find('.code-description-div').first().css({'max-height': (height+40)+'px'});
            
            var ele = $(this).parent().parent().find('.code-description-div').first();
            setTimeout(function(){
                ele.css({'max-height': 'unset'});
            }, 500);
        }
        else{
            
            $(this).parent().parent().find('.code-description-div').first().css({'max-height': '0px'});
        }
    });

});