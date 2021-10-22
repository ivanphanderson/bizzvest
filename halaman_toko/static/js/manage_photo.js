

$(document).ready(function (){

    // ketika user menekan tombol +, maka prompt user untuk memilih file yang diinginkan
    $(".add-photo-wrapper").on("click", function (e) {
       $("#file-picker").click();
    });

    // jika user sudah memilih file yang diinginkan, maka submit form tersebut asynchronously
    $("#file-picker:file").change(function (){
        var pick_file_btn = $("#file-picker");

        // jika user tidak menekan tombol cancel
        if (pick_file_btn.get(0).files.length > 0){

            console.log("uploading photos");
            var formData = new FormData($("form#add-new-photo-form").get(0));

            $.ajax({
                url: "/halaman-toko/add-photo",
                type: 'POST',
                data: formData,
                success: function (json_data) {
                    photo_manager_update_content.update_content_from_existing_json(json_data);
                },


                processData: false,
                contentType: false,
                cache: false,
            });
        }
    });

});
