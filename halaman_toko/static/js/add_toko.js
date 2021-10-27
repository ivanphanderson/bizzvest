
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




    function register_click_only_without_drag(jquery_element, event_handler, movement_toleration=7) {
        var init_pos_x;
        var init_pos_y;

        jquery_element.mousedown(function (e) {
            init_pos_x = e.pageX;
            init_pos_y = e.pageY;
        });

        jquery_element.mouseup(function (e) {
            var curr_x = e.pageX;
            var curr_y = e.pageY;

            // calculating its euclidean distance
            var temp_x = (init_pos_x - curr_x);
            var temp_y = (init_pos_y - curr_y);
            if (temp_x * temp_x  +  temp_y * temp_y < movement_toleration * movement_toleration)
                event_handler(e);
        });
    }

    register_click_only_without_drag($('.submit-confirmation-modal .modal-header'), function (e) {
        $('.submit-confirmation-modal .collapsable').slideToggle();
    });

});
