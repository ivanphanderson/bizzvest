$(document).ready(function() {
	function loadFile(event){
		var formData = new FormData($("form#form_image").get(0));
	$.ajax({
		url : "/my-profile/upload-foto",
		type: 'POST',
		data: formData,
		dataType: false,
		contentType: false,
		processData: false,
		cache: false,
		headers: { 'api-key':'myKey' },
		success: function(){
			$("#output").prop("src", URL.createObjectURL(event.target.files[0]));
			$('.preview img').show();
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) { 
			// alert("Status: " + textStatus); alert("Error: " + errorThrown); 
			$("#output").attr("src", URL.createObjectURL(event.target.files[0]));
		}
		
	});
    }
    $("#file").on("change", loadFile);
});

		
$(document).ready(function() {
          
	/* Centering the modal vertically */
	function alignModal() {
		var modalDialog = $(this).find(".modal-dialog");
		modalDialog.css("margin-top", Math.max(0, 
		($(window).height() - modalDialog.height()) / 2));
	}
	$(".modal").on("shown.bs.modal", alignModal);

	/* Resizing the modal according the screen size */
	$(window).on("resize", function() {
		$(".modal:visible").each(alignModal);
	});
});



