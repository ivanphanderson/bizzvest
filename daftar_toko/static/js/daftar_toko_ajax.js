$('.btn-action').click(function(){
    var url = $(this).data("url"); 
    $.ajax({
        url: url,
        dataType: 'json',
        success: function(res) {

            // get the ajax response data
            var data = res.body;

            // update modal content here
            // you may want to format data or 
            // update other modal elements here too
            $('.modal-body').text(data);

            // show modal
            $('#myModal').modal('show');

        },
        error:function(request, status, error) {
            console.log("ajax call went wrong:" + request.responseText);
        }
    });
});

$("#search").keyup(function() {

    // Retrieve the input field text and reset the count to zero
    var filter = $(this).val(),
      count = 0;

    // Loop through the comment list
    $('#card-company div').each(function() {


      // If the list item does not contain the text phrase fade it out
      if ($(this).text().search(new RegExp(filter, "i")) < 0) {
        $(this).hide();  // MY CHANGE

        // Show the list item if the phrase matches and increase the count by 1
      } else {
        $(this).show(); // MY CHANGE
        count++;
      }

    });

  });

  $('#search').keyup(function (event) {
    var query =($('#search').val());

    if (query != '' || query != ' ') {  
      $.ajax({
         type: 'GET',
         url: '{% url "search" %}',
         data: {
           'csrfmiddlewaretoken': '{{ csrf_token }}',
           'q': query
         },
         success: function(data) {
            $('#main-results-search').html(data);
         },
         error: function(data) {
            console.log(data);
         }
       });
    }
  });

  // Removing the element after search
  // and when user clicked another/outside of this element below.

  $(document).click(function(event) {
    $is_inside = $(event.target).closest('#main-results-search').length;

    if( event.target.id == 'search-bar' || $is_inside ) {
      return;
    }else {
      $('#results-bar').remove();
    }
  });

