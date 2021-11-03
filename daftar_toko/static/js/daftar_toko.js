$("#search").keyup(function() {

    // Retrieve the input field text and reset the count to zero
    var filter = $(this).val(),
      count = 0;

    // Loop through the comment list
    $('#cards').each(function() {


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

  $('#search-bar').keyup(function (event) {
    var query =($('#search-bar').val());

    if (query != '' || query != ' ') {  
      $.ajax({
         type: 'GET',
         url: '{% url "search" %}',
         data: {
           'csrfmiddlewaretoken': '{{ csrf_token }}',
           'q': query
         },
         success: function(data) {
            $('#cards').html(data);
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
    $is_inside = $(event.target).closest('#cards').length;

    if( event.target.id == 'search-bar' || $is_inside ) {
      return;
    }else {
      $('#rcards').remove();
    }
  });

