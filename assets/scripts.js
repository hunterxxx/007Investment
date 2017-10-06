$(document).ready(function(){
    
    $popover = $(".message-popover");
    if($popover.length) {
        window.setTimeout(function() {
            $popover.fadeOut(1000);
        }, 2000);
    }

    $('#start-screen').click(function(){
        $('.push-notification').addClass("fade-in");
    });
    
});