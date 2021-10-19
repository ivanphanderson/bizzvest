
$(document).ready(function (){
    var isian_formulir = $(".isian-formulir");
    isian_formulir.on('keydown', function (e) {
        var element = $(this);
        element.addClass("pressed");
    });

    isian_formulir.on('keyup', function (e) {
        var element = $(this);
        element.removeClass("pressed");
    });


    $("#form-submit-btn").click(function() {
        if ($("#is_validate_only").val().toString() !== '0'){
            $('#form-content').submit();
        }
    });

    $("#form-confirm-submit-btn").click(function(){
        $('#form-content').submit();
    });



    // reset modal if it isn't visible
    if (!($('.modal.in').length)) {
        $('.modal-dialog').css({
            top: 0,
            left: 0
        });
    }


    $('#form-problems-modal, #confirm-submit').modal({
        backdrop: false,
        show: true
    });

    var modal_dialog = $(".modal-dialog");
    modal_dialog.draggable({
        handle: ".modal-header"
    });

    $("#confirm-submit-cancel-btn").on('click', function (e){
        $("#is_validate_only").val('1');
    });

    $(".modal-header").css("cursor", "pointer");


});
