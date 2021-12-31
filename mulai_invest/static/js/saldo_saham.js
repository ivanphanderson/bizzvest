function update_saldo2(data) {
  saldo_temp = data.saldo;
  formatted_saldo = (saldo_temp).toLocaleString('ID', {
    style: 'currency',
    currency: 'IDR',
  });
  document.getElementById("saldoSekarang").innerHTML = formatted_saldo;
  document.getElementById("lembar_dimiliki").innerHTML = data.saham_tanam + " Lembar";
  document.getElementById("saham_terjual").innerHTML = data.saham_terjual + " lembar";
  document.getElementById("saham_tersisa").innerHTML = data.saham_tersisa + " lembar";

  $( ".user-saldo" ).load(window.location.href + " .user-saldo" );
}

function load_DER() {
  document.getElementById("DER").innerHTML = "Debt to Equity Ratio = " + parseInt(Math.random()*300 + 1) + "%<br>Usia toko: " + usia_toko + " bulan";
  var harga_saham = parseInt(document.getElementById("company_nilai_saham").textContent);
  var harga_saham_format = ((harga_saham).toLocaleString('ID', {
    style: 'currency',
    currency: 'IDR',
  }));
  document.getElementById("harga_sahams").innerHTML = harga_saham_format;
}

var formatter = new Intl.NumberFormat('ID', {
    style: 'currency',
    currency: 'IDR',
});


window.onload = load_DER();

$("form#beli_saham").submit(function() {
  var saham_dibeli = $('input[name="jumlah_lembar_saham"]').val().trim();
  var id_comp= parseInt(document.getElementById("company_id").textContent);
  var csr = $("input[name=csrfmiddlewaretoken]").val().trim();
 
      if (saham_dibeli) {
          // Create Ajax Call
          $.ajax({
              url: '/mulai-invest/ajax/beli-saham',
              method: "POST",
              data: {
                  'id': id_comp,
                  'jumlah_lembar_saham': saham_dibeli,
                  csrfmiddlewaretoken: csr
              },
              dataType: 'json',
              success: function (data) {
                  if (data.user.status === 'success') {
                      update_saldo2(data.user);
                      document.getElementById("saldo_kurang").innerHTML = "Transaksi Anda berhasil 🥳";
                      $('form#beli_saham').trigger("reset");
                  } else{
                      alert(data.user.message);
                      document.getElementById("saldo_kurang").innerHTML = data.user.message;
                  }
              }
          });
      } else {
          alert("All fields must have a valid value.");
      }
  return false;
});
