$("#btnsave").on('click', function() {
    console.log("Save Button Clicked")
    let output = "";
    let question = $("#pertanyaan").val();
    let name = $("#nama").val();
    let csr = $("input[name=csrfmiddlewaretoken").val();

    if (name != "" & pertanyaan != "") {
        dataFaq = { nama: name, pertanyaan: question, csrfmiddlewaretoken: csr };
        $.ajax({
            url: "save/",
            method: "POST",
            data: dataFaq,
            dataType: "json",
            success: function (data) {
                ask = data.pertanyaan_data
                if(data.status == "Save"){
                    $("msg").text("Pertanyaan telah terkirim!")
                    $("msg").show();
                    $("#data_pertanyaan").empty();
                    for (i=0; i<ask.length; i++){
                        output += '<div class="card mt-1 mx-4"> <div class="card-body"> <h6 class="card-title">'
                        + ask[i].pertanyaan + '</h6> <p class="card-text">Pertanyaan dari <b>' + ask[1].nama + '</b></p></div></div><br>'
                    }

                    $("#data_pertanyaan").html(output);

                    $("form")[0].reset();

                }
            }
        });
    }
});