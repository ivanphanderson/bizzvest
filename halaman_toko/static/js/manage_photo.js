$(document).ready(function (){
    photo_manager = photo_manager_1;


    var get_toast_instance = (jquery_toast_element=$(".toast")) => bootstrap.Toast.getInstance(jquery_toast_element[0]);
    window.debug__get_toast_instance = get_toast_instance;

    function clear_toast_timeout_if_exist(jquery_toast_element=$(".toast")){
        clearTimeout(get_toast_instance(jquery_toast_element)._timeout);
    }


    // ketika user menekan tombol +, maka prompt user untuk memilih file yang diinginkan
    $(".add-photo-wrapper").on("click", function (e) {
        var temp = $("#file-picker");
        temp[0].value = null;
        temp[0].click()
    });


    // jika user sudah memilih file yang diinginkan, maka submit form tersebut asynchronously
    $("#file-picker:file").change(function (){
        var pick_file_btn = $("#file-picker");

        if (photo_manager.is_currently_sending_ajax()) {
            photo_manager.error_handler('busy', null, photo_manager.busy_msg);
            return false;
        }
        photo_manager.is_currently_sending_ajax(true);
        photo_manager.misc_handler('uploading', 'uploading the selected photo(s)');

        // jika user tidak menekan tombol cancel
        if (pick_file_btn.get(0).files.length > 0){

            if (pick_file_btn.get(0).files.length + photo_manager.manager_items().length > 12){
                photo_manager.error_handler('illegal-uploading', null,
                    "Sorry, you can't have more than 12 photos");
                return;
            }

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
        clear_toast_timeout_if_exist();

        console.log(" =========== start ============");
        console.log(type);
        console.log(xhr);
        console.log(text_status);
        console.log(error_thrown);
        console.log(" =========== end ============");

        if (type === "busy") {
            $(".toast #toast-msg").text(text_status);
            console.log('asdfgh');
        } else if (type === "illegal-uploading")
            $(".toast #toast-msg").text(text_status);
        else if (xhr.readyState === 0)  // masalah koneksi
            $(".toast #toast-msg").text("Sorry, we encountered a connection problem");
        else if (xhr.readyState === 4)  // status code error
            $(".toast #toast-msg").text(xhr.statusText + ":  " + xhr.responseText);
        else
            $(".toast #toast-msg").text("Sorry, we encountered an unknown error");

        $(".toast").toast("show");
    }

    photo_manager.success_handler = function (type, message){
        clear_toast_timeout_if_exist();

        if (type==="deleting")
            $(".toast #toast-msg").text("the photo has been deleted successfully");
        else if (type === "reordering")
            $(".toast #toast-msg").text("the photos' order has been saved");
        else if (type === "uploading")
            $(".toast #toast-msg").text("the photo(s) has been uploaded");
        else
            return;

        $(".toast").toast("show");
    }

    photo_manager.misc_handler = function (type, message) {
        clear_toast_timeout_if_exist();

        $(".toast #toast-msg").text(message);
        $(".toast").toast("show");
    }



    $('.toast').toast({delay:2500});



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



    /* Mengurus layout */

    var readjust_photo_manager = function (e) {
        var photo_manager_container = $("#photo-manager-container");
        var photo_manager_container_width = photo_manager_container.innerWidth();  // assume that the padding is always zero
        var photo_manager = $(".photo-manager");

        var photo_manager_item = $(".photo-manager-items").get(0);
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
