var saldo = parseInt(document.getElementById("user_saldo").textContent);

$("form#updateUser").submit(function() {
    var saldoInput = $('input[name="saldo"]').val().trim();
    // var saldo = parseInt(document.getElementById("user_saldo").textContent);
    // var saldo_temp = parseInt(saldo) + parseInt(saldoInput);
    var csr = $("input[name=csrfmiddlewaretoken]").val().trim();

    if (saldoInput) {
        // Create Ajax Call
        $.ajax({
            url: '/mulai-invest/ajax/update-saldo',
            method: "POST",
            data: {
                'saldo': saldoInput,
                csrfmiddlewaretoken: csr
            },
            dataType: 'json',
            success: function (data) {
                if (data.user.status==='success') {
                    update_saldo(data.user);
                } else {
                    alert(data.user.message)
                }
            }
        });
    } else {
        alert("All fields must have a valid value.");
    }

    $('form#updateUser').trigger("reset");
    $('#myModals').modal('hide');
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
    set_body();
    return false;
});

// Handle bug in modal (modal is not showing), i don't understand why such bug occur :(
var pls_btn = document.getElementById('plus_btn')
pls_btn.addEventListener("click", () => {
    setTimeout(function(){
        document.getElementsByTagName("body")[0].style.overflow = "hidden"
        // if($('.modal-backdrop').length<2){
        //     $('body').append('<div class="modal-backdrop fade show" id="aneh"></div>');
        // }
    }, 200);
    setTimeout(function(){
        const my_modal = document.getElementById("myModals");
        const my_modal_display = my_modal.style.display;
        
        if(my_modal_display.trim() === "none"){
            my_modal.classList.remove("show");
            my_modal.style.display="block";
            setTimeout(function(){
                my_modal.classList.add("show");
            }, 100);
        }
        
    }, 300);
});

// Handle bug in modal (modal is not showing), i don't understand why such bug occur :(
var pls_btn = document.getElementById('close_modal')
pls_btn.addEventListener("click", () => {
    setTimeout(function(){
      const my_modal = document.getElementById("aneh");
      if(my_modal){
          $('#aneh').remove();
      }
    }, 300);
});

function set_body(){
    
    setTimeout(function(){
            document.getElementsByTagName("body")[0].style = "";
        
    }, 200);   
}


function update_saldo(data) {
  saldo_temp = data.saldo;
  formatted_saldo = (saldo_temp).toLocaleString('ID', {
    style: 'currency',
    currency: 'IDR',
  });
  document.getElementById("saldoSekarang").innerHTML = formatted_saldo;
  $( ".user-saldo" ).load(window.location.href + " .user-saldo" );
}

window.onload = update_saldo({'saldo': saldo});
