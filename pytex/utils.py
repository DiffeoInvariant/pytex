import re
import unicodedata
from typing import List

_color_registry = {}
_inverse_color_registry = {}

newline = '////'


unicode_supers = {'\u2070'           : '0',
                        #f'\N{DEGREE SIGN}' : '0',
                        f'\N{SUPERSCRIPT ONE}' : '1',
                        f'\N{SUPERSCRIPT TWO}' : '2',
                        f'\N{SUPERSCRIPT THREE}': '3',
                        f'\N{SUPERSCRIPT FOUR}': '4',
                        f'\N{SUPERSCRIPT FIVE}': '5',
                        f'\N{SUPERSCRIPT SIX}' : '6',
                        f'\N{SUPERSCRIPT SEVEN}' : '7',
                        f'\N{SUPERSCRIPT EIGHT}' : '8',
                        f'\N{SUPERSCRIPT NINE}' : '9'}



unicode_subs = {f'\N{SUBSCRIPT ZERO}' : '0',
                      f'\N{SUBSCRIPT ONE}' : '1',
                      f'\N{SUBSCRIPT TWO}' : '2',
                      f'\N{SUBSCRIPT THREE}': '3',
                      f'\N{SUBSCRIPT FOUR}': '4',
                      f'\N{SUBSCRIPT FIVE}': '5',
                      f'\N{SUBSCRIPT SIX}' : '6',
                      f'\N{SUBSCRIPT SEVEN}' : '7',
                      f'\N{SUBSCRIPT EIGHT}' : '8',
                      f'\N{SUBSCRIPT NINE}' : '9'}

unicode_specials = {'\u20D7' : '\\vec'}


def replace_special_chars(string):
    for i, char in enumerate(string):
        if char in unicode_specials.keys():
            tmp = string[:i] + unicode_specials[char] + string[i:]
            string = tmp
    return string


def replace_superscripts(string):
    N = len(string)
    cpy = ''
    i = 0
    while i < N:
        char = string[i]
        if char in unicode_supers.keys():
            making_num = True
            num = '^{' + unicode_supers[char]
            digits = 1
            while i + digits < N and making_num:
                nextchar = string[i+digits]
                if nextchar in unicode_supers.keys():
                    num += unicode_supers[nextchar]
                    digits += 1
                else:
                    making_num = False

                i += digits - 1

            num += '}'
            cpy += num

        else:
            cpy += char

        i += 1

    return cpy


def replace_subscripts(string):
    N = len(string)
    cpy = ''
    i = 0
    while i < N:
        char = string[i]
        if char in unicode_subs.keys():
            making_num = True
            num = '_{' + unicode_subs[char]
            digits = 1
            while i + digits < N and making_num:
                nextchar = string[i+digits]
                if nextchar in unicode_subs.keys():
                    num += unicode_subs[nextchar]
                    digits += 1
                else:
                    making_num = False

                i += digits - 1

            num += '}'
            cpy += num

        else:
            cpy += char

        i += 1

    return cpy

def replace_supers_and_subs(string):
    return replace_superscripts(replace_subscripts(string))

def view_registered_colors():
    for name in _color_registry.keys():
        print(f"{name} = {_color_registry[name]}")


def _split_at_color(string: str) -> List[bytes]:
    return string.encode('ascii').split(b'\x1b[')

class NotAColorError(ValueError):
    pass


def _get_color_def(string: bytes) -> str:
    strval = str(string,'ascii')
    if not strval[0].isdigit():
        raise NotAColorError
    if ';' not in strval:
        raise NotAColorError
    pos = strval.find('m')
    if pos == -1:
        raise NotAColorError
    return strval[:pos]

def _register_color(name,value) -> None:
    _color_registry[name] = value
    _inverse_color_registry[value] = name

    

def is_color_registered(name) -> bool:
    try:
        val = _color_registry[name]
        return True
    except KeyError:
        return False

def get_color(name) -> str:
    return _color_registry[name]

def get_color_name(registered_color) -> str:
    if _inverse_color_registry[registered_color] is None:
        raise ValueError

    return _inverse_color_registry[registered_color]


class ColorAlreadyRegisteredError(ValueError):
    pass


def _register_colorstring(string: bytes, colorname: str) -> None:
    if colorname in _color_registry and _color_registry[colorname] is not None:
        raise ColorAlreadyRegisteredError
    try:
        if not is_color_registered(colorname):
            _register_color(colorname,_get_color_def(string))
    except NotAColorError:
        raise
        #print(f"Error: Tried to register a color from the string {string}, but it does not start with a color modifier!")


    
    
def register_colors(string: str, names: List[str]) -> None:
    '''
    takes in a string to split at each color definition, then register each unique color
    '''
    bstrings = _split_at_color(string)
    cstrings = set()
    for bstr in bstrings:
        try:
            cd = _get_color_def(bstr)
            cstrings.add(cd)
        except NotAColorError:
            continue

    if len(cstrings) > len(names):
        raise ValueError(f"There are {len(cstrings)} different color definitionsto register, but you only provided {len(names)} names!")

    for i,cst in enumerate(cstrings):
        if is_color_registered(cst):
            continue
        try:
                _register_color(cst,names[i])
        except ColorAlreadyRegisteredError:
            continue
     
            

def remove_colors(string: str) -> str:
    bstr = string.encode('ascii').split(b'\x1b[')
    sstr = [None]*len(bstr)
    for i in range(len(bstr)):
        sstr[i] = str(bstr[i],'ascii')
        for color in _color_registry:
            sstr[i] = sstr[i].replace(color,'')

    return ''.join(sstr)

            
    
#def get_pytest_header(pytest_out_lines):
'''
version of the code at https://github.com/FEniCS/ufl/blob/master/ufl/formatting/printing.py, but this actually works
'''

def get_ufl_form_info(form) -> str:
    from ufl.form import Form
    from ufl.integral import Integral
    from ufl.formatting.printing import integral_info
    from ufl.log import error as uflerr

    if not isinstance(form,Form):
        uflerr(f"Expecting a ufl.Form, in ufl_form_info, got a {type(form)}")

    args = form.arguments()
    coeffs = form.coefficients()

    fi =  "Form info:\n"
    fi += f"  rank:                   {len(args)}\n"
    fi += f"  num_coefficients:       {len(coeffs)}\n"

    for c in coeffs:
        try:
            nm = c._name
            ct = c._count
            fi += f"\n  Coefficient {ct} is named {nm}"
        except AttributeError:
            fi += f"\n  {c._repr} (unnamed)"

    fi += "\n"

    integrals = form.integrals()
    int_types = sorted(set(it.integral_type() for it in integrals))
    for itype in int_types:
        ibts = form.integrals_by_type(itype)
        for itg in ibts:
            fi += integral_info(itg)
            fi += "\n"
    #post-processing
    fi = fi.replace('#','')
    
    
    return fi

    


