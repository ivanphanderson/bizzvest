$(document).ready(function (){
    all_photo_manager_items = [];

    $.get('/halaman-toko/edit-photos?id=' + company_id + '&ajax_get_json', function (response){
        for (let i = 0; i < response.length; i++) {
            var temp = new PhotoManagerItems($(".photo-manager")[0]);
            temp.set_photo_src(response[i].fields.img);
            all_photo_manager_items.push(temp);
        }

        console.log(response);
    });

});

console.log("HELO");


class PhotoManagerItems{
    constructor(jquery_parent_div) {
        this.parent = jquery_parent_div;
        var template = $("#photo-manager-items-template");
        this.element = template.clone()[0];
        this.element = this.element.content.cloneNode(true);
        this.element = $(this.element.querySelector("div"));

        console.log(this.element.get(0));
        this.parent.appendChild(this.element.get(0));
        this.photo_url = "";
    }


    set_photo_src(src){
        this.photo_url = src;
        this.element.css('background-img', 'url("' + src + '")')
    }



}


