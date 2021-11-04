var saldo = parseInt(document.getElementById("user_saldo").textContent);
// {% if user.is_authenticated %}
//     saldo={{user.profile.saldo}};
// {% endif %}

$("form#updateUser").submit(function() {
// var idInput = $('input[name="formId"]').val().trim();
var saldoInput = $('input[name="saldo"]').val().trim();
// saldoInput = (saldoInput.substring(0, saldoInput.length-3)).replace(/\D/g,'');
// console.log(saldoInput);
// var currUser = {{user.id}};
saldo = parseInt(saldo)+parseInt(saldoInput);
if (saldoInput) {
    // Create Ajax Call
    $.ajax({
        url: '/mulai-invest/ajax/update-saldo',
        data: {
            'saldo': saldoInput,
            // 'currUser': currUser
        },
        dataType: 'json',
        success: function (data) {
            if (data.user) {
              update_saldo();
            }
        }
    });
    } else {
    // alert("All fields must have a valid value.");
}
$('form#updateUser').trigger("reset");
$('#myModal').modal('hide');
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
        if($('.modal-backdrop').length<2){
            $('body').append('<div class="modal-backdrop fade show" id="aneh"></div>');
        }
    }, 200);
    setTimeout(function(){
        const my_modal = document.getElementById("myModal");
        const my_modal_display = my_modal.style.display;
        
        console.log(my_modal_display);
        if(my_modal_display.trim() === "none"){
            my_modal.classList.remove("show");
            my_modal.style.display="block";
            setTimeout(function(){
                my_modal.classList.add("show");
            }, 100);
        }
        
    }, 300);
    
    // const my_modal = document.getElementById("myModal");
    // my_modal.style.display="block";
    // fade(my_modal);
});

// Handle bug in modal (modal is not showing), i don't understand why such bug occur :(
var pls_btn = document.getElementById('close_modal')
pls_btn.addEventListener("click", () => {
    setTimeout(function(){
      const my_modal = document.getElementById("aneh");
      // const my_modal_display = my_modal.style.display;
      
      // console.log(my_modal_display);
      if(my_modal){
          // my_modal.classList.remove("modal-backdrop", "fade", "show");
          $('#aneh').remove();
          // my_modal.style.display="block";
          // setTimeout(function(){
              // my_modal.classList.add("show");
          // }, 100);
      }
    }, 300);
    // setTimeout(function(){
    //     const my_modal = document.getElementById("myModal");
    //     const my_modal_display = my_modal.style.display;
        
    //     console.log(my_modal_display);
    //     if(my_modal_display.trim() === "none"){
    //         my_modal.classList.remove("show");
    //         my_modal.style.display="block";
    //         setTimeout(function(){
    //             my_modal.classList.add("show");
    //         }, 100);
    //     }
        
    // }, 300);
    
    // const my_modal = document.getElementById("myModal");
    // my_modal.style.display="block";
    // fade(my_modal);
});

function set_body(){
    
    setTimeout(function(){
        // var is_modal_open_exist = document.getElementsByClassName('modal-open');
        // if (is_modal_open_exist.length > 0) {
        //     console.log("cde");
        // } 
            console.log("abc");
            document.getElementsByTagName("body")[0].style = "";
        
    }, 200);   
}


function update_saldo() {
  saldo_temp = saldo;
  formatted_saldo = (saldo_temp).toLocaleString('ID', {
    style: 'currency',
    currency: 'IDR',
  });
  document.getElementById("saldoSekarang").innerHTML = formatted_saldo;
  $(".lembar_saham").load(window.location.href + " .lembar_saham");
  $( ".refresh" ).load(window.location.href + " .refresh" );
}

function load_DER() {
  // document.getElementById("DER").innerHTML = "Debt to Equity Ratio = " + parseInt(Math.random()*300 + 1) + "%\nusia toko: " + usia_toko;
  update_saldo();
  // console.log({{owner_account.username}});
  // console.log("abc");
}

var formatter = new Intl.NumberFormat('ID', {
style: 'currency',
currency: 'IDR',

// These options are needed to round to whole numbers if that's what you want.
//minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
//maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
});



var a = formatter.format(2500); /* $2,500.00 */
console.log(a);
console.log((2500).toLocaleString('ID', {
style: 'currency',
currency: 'IDR',
})); /* $2,500.00 */

window.onload = load_DER();