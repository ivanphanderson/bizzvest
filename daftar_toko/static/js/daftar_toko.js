$(document).ready(function() {
  $('#search-bar').keyup(function() {
    console.log("TERCETAK");
    $.ajax({ 
      url: "/daftar-toko/search/",
      type: "POST",
      data: {
        'search_text': $('#search-bar').val(),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
      },
      dataType: 'json',
      success: function (data){
        $('.cards').empty()
        console.log("DAH SAMPE SINI")
        console.log(data)
        result = data.company_search;
        output = '';
        console.log(result);
        if(result.length <= 0){
          output += '<center><h1>Hasil Pencarian Tidak Ditemukan :(</h1></center>'; 
        }else{
          console.log("OKE");
          console.log(result.length);
          for(i=0; i<result.length; i++){
            output +=`<div class="card" style="cursor:pointer" onclick="location.href='/halaman-toko/?id=${result[i].id}'">
                <div class="card__image-container">
                  <img src="${result[i].get_first_image}" alt="">
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
        }
        $('.cards').append(output);

      },
      error: function (data) {
        console.log("GaGaL");
      }
    });
  });
});



