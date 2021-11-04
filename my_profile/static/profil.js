$(document).ready(function() {
	function loadFile(event){
		var formData = new FormData($("form#form_image").get(0));
		// var csrftoken = $.cookie('csrftoken');
	// var files = $("#file")[0].files[0];
	// files.append('file',files)
	// var jens = URL.createObjectURL(event.target.files[0]);
	
	// function csrfSafeMethod(method) {
	// 	// these HTTP methods do not require CSRF protection
	// 	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	// }

	// $.ajaxSetup({
	// 	beforeSend: function(xhr, settings) {
	// 		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	// 			xhr.setRequestHeader("X-CSRFToken", csrftoken);
	// 		}
	// 	}
	// });
	
	$.ajax({
		url : "/my-profile/upload-foto",
		type: 'POST',
		// data: URL.createObjectURL(event.target.files[0]),
		data: formData,
		// contentType: "image/png",
		dataType: false,
		contentType: false,
		processData: false,
		cache: false,
		headers: { 'api-key':'myKey' },
		success: function(){
			$("#output").prop("src", URL.createObjectURL(event.target.files[0]));
			$('.preview img').show();
		// 	$("#output").get(0).src = URL.createObjectURL(event.target.files[0]);
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) { 
			// alert("Status: " + textStatus); alert("Error: " + errorThrown); 
			$("#output").attr("src", URL.createObjectURL(event.target.files[0]));
		}
		
	});
    }
    $("#file").on("change", loadFile);
});
// var loadfile = function(event){
	
// 	// var image = document.getElementById("output")
// 	// var image = document.getElementById("output");
	
	
// 	var formData = new FormData($("form#form_image").get(0));
// 	var files = $("#file")[0].files[0];
// 	files.append('file',files)
// 	// var jens = URL.createObjectURL(event.target.files[0]);
	
// 	$.ajax({
// 		url : "../my-profile/ganti-profil",
// 		type: "POST",
// 		// data: URL.createObjectURL(event.target.files[0]),
// 		data: formData,
// 		// contentType: "image/png",
// 		contentType: false,
// 		processData: false,
// 		success: function loadfile(event){
// 			$("#output").attr("src", URL.createObjectURL(event.target.files[0]));
// 			$('.preview img').show();
// 		// 	$("#output").get(0).src = URL.createObjectURL(event.target.files[0]);
// 		},
// 		error: function(XMLHttpRequest, textStatus, errorThrown) { 
// 			// alert("Status: " + textStatus); alert("Error: " + errorThrown); 
// 			$("#output").attr("src", URL.createObjectURL(event.target.files[0]));
// 		}
		
// 	});
	
// };


// var loadFile = function (event) {
// 	var image = document.getElementById("output")
// 	// var image = document.getElementById("output");
// 	image.src = URL.createObjectURL(event.target.files[0]);
	
//   }

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



