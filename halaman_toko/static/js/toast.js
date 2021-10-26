// need bootstrap and jquery

var get_toast_instance = (jquery_toast_element) => bootstrap.Toast.getInstance(jquery_toast_element[0]);

function clear_toast_timeout_if_exist(jquery_toast_element){
    clearTimeout(get_toast_instance(jquery_toast_element)._timeout);
}

function show_toast(message, status=0) {  // status 0: normal, 1: error, 2: success
    var toast_el = $("#my-toast");
    clear_toast_timeout_if_exist(toast_el);


    toast_el.removeClass("normal-msg");
    toast_el.removeClass("error-msg");
    toast_el.removeClass("success-msg");
    toast_el.addClass(['normal-msg', 'error-msg', 'success-msg'][status]);

    $("#toast-msg").html(message);
    toast_el.toast("show");
}