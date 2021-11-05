// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("ct-button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("ct-close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
    $("form")[0].reset();
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

$("#savemsg").on('click', function(e) {
    console.log("Send Button Clicked");
    let mail = $("#email").val();
    let pesan = $("#pesan").val();
    let csr = $("input[name=csrfmiddlewaretoken]").val();
    e.preventDefault();

    if (mail != "" & pesan != "") {
        $.ajax({
            url: "save-message/",
            method: "POST",
            data:{ 
                email: mail, 
                message: pesan, 
                csrfmiddlewaretoken: csr 
            },
            dataType:"json",
            success: function (data) {
                if(data.status == "Save"){
                    console.log("Successfully added a message!");
                    alert("Pesan telah dikirim!");
                    $("form")[0].reset();
                    modal.style.display = "none";
                }
            }
        });
    }
});
