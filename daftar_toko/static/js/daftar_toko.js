$(document).ready(function() {
  $('#search-bar').keyup(function() {
    console.log("TECETAK");
    $.ajax({ 
      type: "POST",
      url: "search/",
      data: {
        'search_text': $('#search-bar').val(),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
      },
      dataType: 'html',
      succes: function (data){
        $('#search-results').html(data);
      },
    });
  });
});



