var saham_sisa = parseInt(document.getElementById("saham_tersisaa").textContent);
var saldo = parseInt(document.getElementById("user_saldo").textContent);


function update_saldo() {
  saldo_temp = saldo;
  formatted_saldo = (saldo_temp).toLocaleString('ID', {
    style: 'currency',
    currency: 'IDR',
  });
  document.getElementById("saldoSekarang").innerHTML = formatted_saldo;
  $( ".refresh" ).load(window.location.href + " .refresh" );
  $( ".refresh1" ).load(window.location.href + " .refresh1" );
  $( ".refresh2" ).load(window.location.href + " .refresh2" );
}

function load_DER() {
  document.getElementById("DER").innerHTML = "Debt to Equity Ratio = " + parseInt(Math.random()*300 + 1) + "%<br>Usia toko: " + usia_toko + " bulan";
  var harga_saham = parseInt(document.getElementById("company_nilai_saham").textContent);
  var harga_saham_format = ((harga_saham).toLocaleString('ID', {
    style: 'currency',
    currency: 'IDR',
  }));
  document.getElementById("harga_sahams").innerHTML =harga_saham_format;
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
  
  if(sisa_lembar<0){
      alert("Saham yang tersisa pada perusahaan ini hanya " + saham_sisa +" lembar");
      document.getElementById("saldo_kurang").innerHTML = "Saham yang tersisa pada perusahaan ini hanya " + saham_sisa +" lembar";
  }
  else if(saldo_temp<0){
      alert("Saldo Anda tidak cukup 😢");
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
