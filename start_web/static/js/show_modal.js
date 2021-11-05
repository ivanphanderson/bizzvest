$(document).ready(function(){
    $("#myModal").modal('show');
});

$(document).ready(function(e) {
    $('#myModal').on('hidden.bs.modal', function(e) {
        window.location.href = '/'
    });
});