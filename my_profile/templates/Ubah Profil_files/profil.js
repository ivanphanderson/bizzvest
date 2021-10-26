var loadFile = function (event) {
	var image = document.getElementById("output");
	image.src = URL.createObjectURL(event.target.files[0]);
  }

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



