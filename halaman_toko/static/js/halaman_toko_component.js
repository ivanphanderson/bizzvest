
$(document).ready(function (){

    $(function() {
        $('#company_photos_carousel').each(function(){
            $(this).carousel({
                interval: 7000
            });
        });
    });

    function carousel_background_updates(active=true) {
        var carousel_item, background_el;
        if (active) {
            carousel_item = $('#company_photos_carousel .carousel-item.active .company_photos_carousel_item_img');
            background_el = $("#company_photos_carousel .carousel-item.active .carousel-item-extra-background");
        }else {
            carousel_item = $('#company_photos_carousel .carousel-item .company_photos_carousel_item_img');
            background_el = $("#company_photos_carousel .carousel-item .carousel-item-extra-background");
        }

        for (let i = 0; i < carousel_item.length; i++) {
            var temp2 = getComputedStyle(carousel_item.get(i)).getPropertyValue("--company_photos_carousel_background_img");
            $(".carousel-adaptive-background-component").css("background-image", temp2);
            background_el.eq(i).css("background-image", temp2);
        }
    }

    $('#company_photos_carousel').on('slid.bs.carousel', carousel_background_updates)
    carousel_background_updates(false);




    $("#save_btn").on('click', function(e){
        var el =  $("#company_description");
        var description_content = get_text_with_correct_new_lines(el);

        if (description_content.length === 0){
            alert("sorry, the description cannot be empty");
            return;
        }

        el.html(get_text_with_correct_new_lines(el, false));
        $("#company_description").attr('contenteditable','false');
        $(".control_btn").prop('disabled', true);


        $.ajax("/halaman-toko/save-edited-company-form", {
            type: "POST",
            data: {
                'id': company_id,
                'deskripsi': description_content,
                'csrfmiddlewaretoken': csrf_token,
            },
            statusCode: {
                200: function (response) {
                    $("#control_btn_container").toggleClass("editing_mode");
                    $(".control_btn").prop('disabled', false);
                },
                400: function (response) {
                    $("#company_description").attr('contenteditable','true');
                    $(".control_btn").prop('disabled', false);
                    alert(response.responseText);
                },
                404: function (response) {
                    $("#company_description").attr('contenteditable','true');
                    $(".control_btn").prop('disabled', false);
                    alert(response.responseText);
                }
            }, success: function () {
            },
        });
    });

    $("#edit_btn").on('click', function(e){
        $("#control_btn_container").toggleClass("editing_mode");
        $("#company_description").attr('contenteditable','true');
    });

});
function company_description_KeyPress(){
    var el =  $("#company_description");
    var description_content = get_text_with_correct_new_lines(el, false);
    description_content
    el.html(description_content);
}

function get_text_with_correct_new_lines(element, decode_tag=true){
    const convertToText = (str = '') => {  // credit: https://gist.github.com/nathansmith/86b5d4b23ed968a92fd4
        // Ensure string.
        let value = String(str);

        // Convert encoding.
        value = value.replace(/&nbsp;/gi, ' ');
        value = value.replace(/&amp;/gi, '&');

        // Replace `<br>`.
        value = value.replace(/<br>/gi, '\n');

        // Replace `<div>` (from Chrome).
        value = value.replace(/<div>/gi, '\n');

        // Replace `<p>` (from IE).
        value = value.replace(/<p>/gi, '\n');

        // Remove extra tags.
        value = value.replace(/<(.*?)>/g, '');

        // Trim each line.
        value = value
            .split('\n')
            .map((line = '') => {
                return line.trim();
            })
            .join('\n');

        // No more than 2x newline, per "paragraph".
        value = value.replace(/\n\n+/g, '\n\n');

        // Clean up spaces.
        value = value.replace(/[ ]+/g, ' ');
        value = value.trim();


        // decode
        value = value.replace(/&amp;/gi, '&');
        if (decode_tag) {
            value = value.replace(/&gt;/gi, '>');
            value = value.replace(/&lt;/gi, '<');
        }

        // Expose string.
        return value;
    };
    return convertToText(element.html());

    /*var str_builder = [];

    let contents = element.contents();

    for (let i = 0; i < contents.length; i++) {
        if (contents[i].nodeType === Node.ELEMENT_NODE){
            var tag_name = contents[i].tagName;
            if (tag_name === 'DIV' || tag_name === 'P' || tag_name === 'BR'){

                if (tag_name === "BR"){
                    str_builder.push("\n");
                }

                if (contents.tagName !== 'BR'){
                    var returned = get_text_with_correct_new_lines(
                        $(contents[i])
                    );
                    str_builder.push(returned);
                }
            }else {
            }
        }else if (contents[i].nodeType === Node.TEXT_NODE){
            str_builder.push(contents[i].wholeText);
        }else if (typeof(contents[i]) === "undefined" || contents[i] === "undefined"){

        }else{
            // str_builder.push(contents[i].toString());
            console.log("unhandled node type: " + contents[i].nodeType + "   " + typeof(contents[i]) + "  "
                + contents[i]);
        }
    }
    return str_builder.join("");*/
}