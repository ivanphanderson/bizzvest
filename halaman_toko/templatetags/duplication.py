from typing import Any

from django import template
from datetime import datetime

from django.template import TemplateSyntaxError, NodeList
from django.template.base import Token, Parser, NodeList

register = template.Library()

""" ibarat fungsi pada bahasa pemrograman yang berguna untuk mengubah WET code menjadi DRY code, ini juga dipakai
untuk mengubah WET html code menjadi DRY html code, namun tetap bisa menambahkan class spesifik pada tag, serta
tidak perlu mengandalkan tag <template> pada HTML dimana tag tersebut memerlukan bantuan JavaScript yang cukup rumit.


CONTOH PENGGUNAAN

###################   Template:   ###################

{% define_duplication 'duplikasi_1' %}
    <div class="wrapper {{ extra_class }}"> 
        <h3> Halo dunia! Apakabar?!? </h3>
        <p> Senang bertemu denganmu! </p>
    </div>
{% end_define_duplication &}


{% define_duplication 'duplikasi_2' %}
    <div class="wuppy {{ extra_class }}"> 
        <h5> Sst! Jangan berisik. </h3>
    </div>
{% end_define_duplication &}


{% instantiate_duplication 'duplikasi_1' 'kelas_1' %}
Semua yang ada disini tidak akan dirender
{% end_instantiate_duplication %}


{% instantiate_duplication 'duplikasi_2' 'kelas_2' %}
Semua yang ada disini tidak akan dirender
{% end_instantiate_duplication %}


{% instantiate_duplication 'duplikasi_2' 'kelas_3' %}
Semua yang ada disini tidak akan dirender
{% end_instantiate_duplication %}


{% instantiate_duplication 'duplikasi_1' 'kelas_4' %}
Semua yang ada disini tidak akan dirender
{% end_instantiate_duplication %}





###################   Hasil setelah dirender:   ###################

    <div class="wrapper kelas_1"> 
        <h3> Halo dunia! Apakabar?!? </h3>
        <p> Senang bertemu denganmu! </p>
    </div>
    
    <div class="wuppy kelas_2"> 
        <h5> Sst! Jangan berisik. </h3>
    </div>
    
    <div class="wuppy kelas_3"> 
        <h5> Sst! Jangan berisik. </h3>
    </div>
    
    <div class="wrapper kelas_4"> 
        <h3> Halo dunia! Apakabar?!? </h3>
        <p> Senang bertemu denganmu! </p>
    </div>

"""

"""
    JANGAN LUPA SETIAP DAFTAR CUSTOM TEMPLATE TAG BARU, HARUS RESTART manage.py runserver
"""



class DefineDuplicationNode(template.Node):
    ALL_DEFINED_DUPLICATIONS = {}

    def __init__(self, id, nodelist: NodeList):
        self.nodelist: NodeList = nodelist
        self.id = id
        self.__class__.ALL_DEFINED_DUPLICATIONS[self.id] = self

    def render(self, context):  # dipanggil oleh django setiap kali django menemukan tag ini
        return ""  # jangan mengembalikan apapun. Semua yang ada di dalam tag ini tidak akan dirender

    def render_me(self, context):  # dipanggil oleh InstantiateDuplication
        rendered = self.nodelist.render(context)  # render child nodes, dan dapatkan html hasil render-nya
        return rendered  # mengoutputkan hasil render


class InstantiateDuplication(template.Node):
    def __init__(self, target_duplication_id:str, extra_class:str, nodelist:NodeList):
        self.nodelist = nodelist
        self.extra_class = str(extra_class)
        self.target_duplication_id = str(target_duplication_id)

    def render(self, context):
        context['extra_class'] = self.extra_class
        defined_duplication = DefineDuplicationNode.ALL_DEFINED_DUPLICATIONS[self.target_duplication_id]
        return defined_duplication.render_me(context)



@register.tag
def define_duplication(parser:Parser, token:Token) -> DefineDuplicationNode:
    temp = token.split_contents()  # split whitespace, tapi tidak men-split whitespace yang ada di dalam string
    try:
        nama_tag, duplication_id = temp
    except ValueError:
        raise TemplateSyntaxError("define_duplication takes one string arguments: duplication_id")

    # parse semua node ke dalam nodelist sampai akhirnya ketemu token end_define_duplication
    nodelist: NodeList = parser.parse(("end_define_duplication",))

    # Kita buang (jangan dimasukkan ke rendered html) token end_define_duplication tersebut
    parser.delete_first_token()  # first token = token pertama pada posisi kursor saat ini

    duplication_id = duplication_id[1:-1]  # menghapus tanda kutip di awal dan di akhir
    return DefineDuplicationNode(duplication_id, nodelist)



@register.tag
def instantiate_duplication(parser:Parser, token:Token) -> InstantiateDuplication:
    temp = token.split_contents()  # split whitespace, tapi tidak men-split whitespace yang ada di dalam string
    try:
        nama_tag, duplication_id, extra_class = temp
    except ValueError:
        raise TemplateSyntaxError("define_duplication takes two string arguments: target_duplication_id and extra_class")

    nodelist: NodeList = parser.parse(("end_instantiate_duplication",))
    parser.delete_first_token()  # first token = token pertama pada posisi kursor saat ini

    duplication_id = duplication_id[1:-1]  # menghapus tanda kutip di awal dan di akhir
    extra_class = extra_class[1:-1]  # menghapus tanda kutip di awal dan di akhir
    return InstantiateDuplication(duplication_id, extra_class, nodelist)

