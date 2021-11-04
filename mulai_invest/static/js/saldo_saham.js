var saham_sisa = parseInt(document.getElementById("saham_tersisaa").textContent);
var saldo = parseInt(document.getElementById("user_saldo").textContent);
// {% if user.is_authenticated %}
//     saldo={{user.profile.saldo}};
// {% endif %}


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
  document.getElementById("DER").innerHTML = "Debt to Equity Ratio = " + parseInt(Math.random()*300 + 1) + "%\nusia toko: " + usia_toko;
  update_saldo();
  // console.log({{owner_account.username}});
  // console.log("abc");
}

var formatter = new Intl.NumberFormat('ID', {
    style: 'currency',
    currency: 'IDR',
});




window.onload = load_DER();

$("form#beli_saham").submit(function() {
  var saham_dibeli = $('input[name="jumlah_lembar_saham"]').val().trim();
  var sisa_lembar = parseInt(saham_sisa)-parseInt(saham_dibeli);
  var totalHarga = parseInt(saham_dibeli)*parseInt(document.getElementById("company_nilai_saham").textContent);
  var saldo_temp = parseInt(saldo)-parseInt(totalHarga);
  var id_comp= parseInt(document.getElementById("company_id").textContent);
  
  console.log(saldo_temp);
  if(sisa_lembar<0){
      document.getElementById("saldo_kurang").innerHTML = "Saham yang tersisa pada perusahaan ini hanya " + saham_sisa +" lembar";
  }
  else if(saldo_temp<0){
      document.getElementById("saldo_kurang").innerHTML = "Saldo Anda tidak cukup 😢";
  } else{
      if (saham_dibeli) {
          saldo=parseInt(saldo_temp);
          saham_sisa=sisa_lembar;
          // Create Ajax Call
          $.ajax({
              url: '/mulai-invest/ajax/beli-saham',
              data: {
                  'id': id_comp,
                  'jumlah_lembar_saham': saham_dibeli,
                  'saldo': saldo
              },
              dataType: 'json',
              success: function (data) {
                  if (data.user) {
                      update_saldo();
                  }
              }
          });

      } else {
          alert("All fields must have a valid value.");
      }
      document.getElementById("saldo_kurang").innerHTML = "Transaksi Anda berhasil 🥳";
      $('form#beli_saham').trigger("reset");
  }
  return false;
});