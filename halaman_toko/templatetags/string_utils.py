from django import template
from datetime import datetime

register = template.Library()

@register.filter
def chars_replace(string:str, find_replace_char:str):
    """Me-replace char pada `string` berdasarkan `find_replace_char`.
    find_replace_char haruslah merupakan sebuah string dengan panjang genap.
    Untuk setiap character pada find_replace_char dengan index genap (0, 2, 4, ...),
    akan di cari pada `string` dan kemudian akan direplace dengan character pada index setelahnya (index+1)
    """
    assert len(find_replace_char) % 2 == 0

    string = str(string)  # memastikan sudah berupa string
    for i in range(0, len(find_replace_char), 2):
        string = string.replace(find_replace_char[i], find_replace_char[i+1])

    return string
