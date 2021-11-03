$(document).ready(function (){
    photo_manager = photo_manager_1;


    // ketika user menekan tombol +, maka prompt user untuk memilih file yang diinginkan
    $(".add-photo-wrapper").on("click", function (e) {
        var temp = $("#file-picker");
        temp[0].value = null;
        temp[0].click()
    });


    // jika user sudah memilih file yang diinginkan, maka submit form tersebut asynchronously
    $("#file-picker:file").change(function (){
        var pick_file_btn = $("#file-picker");


        // jika user tidak menekan tombol cancel
        if (pick_file_btn.get(0).files.length > 0){
            if (photo_manager.is_currently_sending_ajax()) {
                photo_manager.error_handler('busy', null, photo_manager.busy_msg);
                return false;
            }

            if (pick_file_btn.get(0).files.length + photo_manager.manager_items().length > 12){
                photo_manager.error_handler('illegal-uploading', null,
                    "Sorry, you can't have more than 12 photos");
                return false;
            }

            photo_manager.is_currently_sending_ajax(true);
            photo_manager.misc_handler('uploading', 'uploading the selected photo(s)');


            console.log("uploading photos");
            var formData = new FormData($("form#add-new-photo-form").get(0));

            $.ajax({  // harus pakai ajax `processData: false, contentType: false` untuk mencegah illegal invocation
                url: "/halaman-toko/add-photo",
                type: 'POST',
                data: formData,
                success: function (json_data) {
                    photo_manager.is_currently_sending_ajax(false);
                    photo_manager.success_handler('uploading', json_data);
                    photo_manager.update_content_from_existing_json(json_data);
                },
                error: function(xhr, text_status, error_thrown){
                    photo_manager.is_currently_sending_ajax(false);
                    photo_manager.error_handler('uploading', xhr, text_status, error_thrown);
                },

                processData: false,
                contentType: false,
                cache: false,
            });
        }
    });


    photo_manager.error_handler = function (type, xhr, text_status, error_thrown){

        if (type === "busy" || type === "illegal-uploading")
            show_toast(text_status, 1);
        else if (xhr.readyState === 0)  // masalah koneksi
            show_toast("Sorry, we encountered a connection problem", 1);
        else if (xhr.readyState === 4)  // status code error
            show_toast(xhr.statusText + ":  " + xhr.responseText, 1);
        else
            show_toast("Sorry, we encountered an unknown error", 1);

    }

    photo_manager.success_handler = function (type, message){
        if (type==="deleting")
            show_toast("the photo has been deleted successfully", 2);
        else if (type === "reordering")
            show_toast("the photos' order has been saved", 2);
        else if (type === "uploading")
            show_toast("the photo(s) has been uploaded", 2);
        else
            return;

        setTimeout(readjust_photo_manager, 150);
    }

    photo_manager.misc_handler = function (type, message) {
        show_toast(message, 0);
    }



    $('.toast').toast({delay:3000});



    var touchtime = 0;
    $(".double-click-mobile-friendly").on("click", function() {
        console.log("click");

        // noinspection EqualityComparisonWithCoercionJS
        if (touchtime == 0) {
            // set first click
            touchtime = new Date().getTime();
        } else {
            // compare first click to this click and see if they occurred within double click threshold
            if (((new Date().getTime()) - touchtime) < 800) {
                // double click occurred

                touchtime = 0;
            } else {
                // not a double click so set as a new first click
                touchtime = new Date().getTime();
            }
        }
    });



    /* ======================= Mengurus layout ======================= */

    var readjust_photo_manager = function (e) {
        var photo_manager_container = $("#photo-manager-container");
        var photo_manager_container_width = photo_manager_container.innerWidth();  // assume that the padding is always zero
        var photo_manager = $(".photo-manager");

        var photo_manager_item = $(".photo-manager-items").get(0);
        if (photo_manager_item == null)
            return;
        var computed_photo_item = getComputedStyle(photo_manager_item);

        var photo_item_width = computed_photo_item.getPropertyValue('--photo-manager-items-size');
        photo_item_width = photo_item_width.replace("px", "").trim();
        var photo_item_margin = computed_photo_item.getPropertyValue('--photo-manager-items-margin');
        photo_item_margin = photo_item_margin.replace("px", "").trim();

        var total_width_each_item = parseInt(photo_item_width) + 2 * parseInt(photo_item_margin);

        var max_number_of_item_per_row = Math.max(1,
            Math.floor((photo_manager_container_width - 40) / total_width_each_item));

        photo_manager.css('display', 'grid');
        photo_manager.css('grid-template-rows', 'repeat(12, auto)');  // 12 = banyak foto maksimum
        photo_manager.css('grid-template-columns', 'repeat(' + max_number_of_item_per_row + ', auto)');
    };

    $(window).resize(readjust_photo_manager);

    try{
        readjust_photo_manager();
    }catch (e) {
        setTimeout(readjust_photo_manager, 200);
    }

});
