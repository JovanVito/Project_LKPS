from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """
    Membagi string menjadi list (array) berdasarkan karakter pemisah.
    Contoh penggunaan di HTML: "A,B,C"|split:","
    """
    return value.split(arg)