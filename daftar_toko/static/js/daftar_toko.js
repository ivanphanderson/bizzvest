$(document).ready(function() {
  if($('#search-bar').val()==''){
    show();
  }
  $('#search-button').on('click', search);
});

function show(){
  $.ajax({
    url: "/daftar-toko/search/",
    success: function(data){
      $('.cards').empty();
      $('#not-found').empty();
      result = data.company_search;
      output = '';
      console.log(result);
        console.log("OKE");
        console.log(result.length);
        for(i=0; i<result.length; i++){
          output +=`<div class="card" style="cursor:pointer" onclick="location.href='/halaman-toko/?id=${result[i].id}'">
              <div class="card__image-container">
                <img src="${result[i].img}" alt="">
              </div>
              <div class="card__content">
                  <span class="card__title">
                    <p class="text--big">
                      ${ result[i].nama_merek }
                  </p>
                  </span>
                  <div class="card__info">
                      <p class="text--medium">${ result[i].nama_perusahaan }</p> 
                  </div>
                  <div>

                  </div>
              </div>
          </div>`
        }
        $('.cards').append(output);

      
    }
  })
}

function search(){
  console.log("TERCETAK");
  $.ajax({ 
    url: "/daftar-toko/search/",
    type: "POST",
    data: {
      'search_text': $('#search-bar').val() ? $('#search-bar').val() : '',
      'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
    },
    dataType: 'json',
    success: function (data){
      $('.cards').empty();
      $('#not-found').empty();
      console.log("DAH SAMPE SINI")
      console.log(data)
      result = data.company_search;
      output = '';
      console.log(result);
      if(result.length <= 0){
        output += '<div id="not-found"><h3>Hasil Pencarian Tidak Ditemukan :(</h3><button id="kembali-button" onclick="show()">Kembali ke Daftar Toko</button></div>';
        $('#not-found').append(output);
      }else{
        console.log("OKE");
        console.log(result.length);
        for(i=0; i<result.length; i++){
          output +=`<div class="card" style="cursor:pointer" onclick="location.href='/halaman-toko/?id=${result[i].id}'">
              <div class="card__image-container">
                <img src="${result[i].img}" alt="">
              </div>
              <div class="card__content">
                  <span class="card__title">
                    <p class="text--big">
                      ${ result[i].nama_merek }
                  </p>
                  </span>
                  <div class="card__info">
                      <p class="text--medium">${ result[i].nama_perusahaan }</p> 
                  </div>
                  <div>

                  </div>
              </div>
          </div>`
        }
        $('.cards').append(output);

      }
      
    },
    error: function (data) {
      console.log("GaGaL");
    }
  });
}

function clearSearch(){
  $('#search-bar').val('');
  show();
}