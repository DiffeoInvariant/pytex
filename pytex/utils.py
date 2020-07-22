import re
import unicodedata
from typing import List


_color_registry = {}
_inverse_color_registry = {}

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
     
            
