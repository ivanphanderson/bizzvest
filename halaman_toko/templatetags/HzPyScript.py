import ast
import traceback
from typing import Any

from django import template
from datetime import datetime

from django.template import TemplateSyntaxError, NodeList, RequestContext
from django.template.base import Token, Parser, NodeList

register = template.Library()

""" Menjalankan script python di dalam template. 
Pakailah perintah cout() untuk mengoutputkan ke dalam template.

"""

"""
    JANGAN LUPA SETIAP DAFTAR CUSTOM TEMPLATE TAG BARU, HARUS RESTART manage.py runserver
"""



class HzPyScriptNode(template.Node):
    def __init__(self, nodelist: NodeList):
        self.nodelist: NodeList = nodelist

    def render(self, context:RequestContext):  # dipanggil oleh django setiap kali django menemukan tag ini
        output_list = []
        def cout(*args, end='\n', separate=' '):
            output_list.append(f"{separate.join(map(str, args))}{end}")

        python_script = self.nodelist.render(RequestContext(context.request, {}))
        variable = context.flatten().copy()
        variable['cout'] = cout
        try:
            exec(python_script, variable)
        except Exception as e:
            with open('log.txt', 'a') as fstream:
                fstream.write("\n\n\n")
                fstream.write(traceback.format_exc())
            return "[error occured. Please check log.txt to debug]"
        return "".join(output_list)


@register.tag
def HzPyScript(parser:Parser, token:Token) -> HzPyScriptNode:
    temp = token.split_contents()  # split whitespace, tapi tidak men-split whitespace yang ada di dalam string
    nodelist: NodeList = parser.parse(("end_HzPyScript",))
    parser.delete_first_token()  # first token = token pertama pada posisi kursor saat ini

    try:
        ast.parse(nodelist.render({}))  # mengecek syntax python yang ada didalamnya
    except SyntaxError as e:
        raise TemplateSyntaxError(traceback.format_exc())

    return HzPyScriptNode(nodelist)

