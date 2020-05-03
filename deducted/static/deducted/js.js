$(document).ready(function(){

    $(window).scroll(function(){

        var scrolled = false;

        if($(window).width()>600){

            if ( ($(document).scrollTop() > ($('.info-div').height()+20)) && !scrolled ){
                
                $('.top-bar-div .logo-div').css({'left': '0', 'transform': 'translate(0)'});
                $('.top-bar-page-title').removeClass('slide-up-disappear');
                $('.top-bar-page-title').show();
                $('.top-bar-page-title').addClass('slide-down-appear');
                scrolled = true;
            }
            else {

                if( $('.top-bar-page-title').css('display')=='block' ) {
                
                    $('.top-bar-div .logo-div').css({'left': '50%', 'transform': 'translate(-50%, 0)'});
                    $('.top-bar-page-title').removeClass('slide-down-appear');
                    $('.top-bar-page-title').addClass('slide-up-disappear');
                    scrolled = false
                    setTimeout(function(){
                        $('.top-bar-page-title').hide();
                    }, 1000);

                }
            }
        }
    });

});