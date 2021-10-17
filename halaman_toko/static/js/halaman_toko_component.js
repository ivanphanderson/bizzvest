$(document).ready(function (){

    $(function() {
        $('#company_photos_carousel').each(function(){
            $(this).carousel({
                interval: 7000
            });
        });
    });

    function carousel_background_updates(active=true) {
        var carousel_item, background_el;
        if (active) {
            carousel_item = $('#company_photos_carousel .carousel-item.active .company_photos_carousel_item_img');
            background_el = $("#company_photos_carousel .carousel-item.active .carousel-item-extra-background");
        }else {
            carousel_item = $('#company_photos_carousel .carousel-item .company_photos_carousel_item_img');
            background_el = $("#company_photos_carousel .carousel-item .carousel-item-extra-background");
        }

        for (let i = 0; i < carousel_item.length; i++) {
            var temp2 = getComputedStyle(carousel_item.get(i)).getPropertyValue("--company_photos_carousel_background_img");
            $(".carousel-adaptive-background-component").css("background-image", temp2);
            background_el.eq(i).css("background-image", temp2);
        }
    }

    $('#company_photos_carousel').on('slid.bs.carousel', carousel_background_updates)
    carousel_background_updates(false);

});