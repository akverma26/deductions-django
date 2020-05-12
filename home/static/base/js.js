$(document).ready(function(){

    var isFixedTopBarShowed = false;
    var ele = $("a[class*='deduction']");

    for( var _ele_ of ele){
        checkAnimation(_ele_, 'deductionAppear');
    }

    checkAnimation($('.top-bar-div .logo-div .title-text'), 'rubberBand');

    $(window).scroll(function(){

        for( var _ele_ of ele){
            checkAnimation(_ele_, 'deductionAppear');
        }

        checkAnimation($('.top-bar-div .logo-div .title-text'), 'rubberBand');

        if ( $(document).scrollTop() > $('.top-bar-div').height()/2 ) {

            if(!isFixedTopBarShowed) {

                isFixedTopBarShowed = true;

                $('.fixed-top-bar .logo').removeClass('bounceOutLeft');
                $('.fixed-top-bar .title').removeClass('bounceOutRight');
                $('.fixed-top-bar .logo').addClass('bounceInLeft');
                $('.fixed-top-bar .title').addClass('bounceInRight');
                // $('.fixed-top-bar').removeClass('fadeOut');
                // $('.fixed-top-bar').addClass('fadeIn');
                $('.fixed-top-bar').css('display', 'flex');
                
                // $('.fixed-top-bar .title').show();
            }
        }
        else {

            if(isFixedTopBarShowed) {

                isFixedTopBarShowed = false;

                $('.fixed-top-bar .logo').removeClass('bounceInLeft');
                $('.fixed-top-bar .title').removeClass('bounceInRight');
                $('.fixed-top-bar .logo').addClass('bounceOutLeft');
                $('.fixed-top-bar .title').addClass('bounceOutRight');
                // $('.fixed-top-bar').removeClass('fadeIn');
                // $('.fixed-top-bar').addClass('fadeOut');

                setTimeout(function(){
                    $('.fixed-top-bar').hide();
                    // $('.fixed-top-bar .title').hide();
                }, 1000);
            }

        }

    });

});

function isElementInViewport(elem) {
    var $elem = $(elem);

    // Get the scroll position of the page.
    var scrollElem = ((navigator.userAgent.toLowerCase().indexOf('webkit') != -1) ? 'body' : 'html');
    var viewportTop = $(scrollElem).scrollTop();
    var viewportBottom = viewportTop + $(window).height();

    // Get the position of the element on the page.
    var elemTop = Math.round( $elem.offset().top );
    var elemBottom = elemTop + $elem.height();

    return ((elemTop < viewportBottom) && (elemBottom > viewportTop));
}

// Check if it's time to start the animation.
function checkAnimation(element, animationClass) {

    var $elem = $(element);

    // If the animation has already been started
    // if ($elem.hasClass(animationClass)) return;

    if (isElementInViewport($elem)) {
        // Start the animation
        
        $elem.addClass(animationClass);
    }
    else {
        $elem.removeClass(animationClass);
    }
}

// Capture scroll events
// $(window).scroll(function(){
   
// })