from .text import TextLines
from .command import Command, UsePackage
from .utils import replace_special_chars, replace_subscripts, replace_superscripts, get_color, get_color_name
from collections.abc import Iterable

class Environment(TextLines):

    __slots__ = ['begin','end','required_packages']
    
    def __init__(self, envtype: str, text_lines: Iterable, name: str = None, starred: bool=False, env_options: Iterable=None, required_packages: Iterable=None):
        #NOTE: required_packages is a list of either strings or tuples of string and Iterable[string] (package name or name and options)
        nm = name if name else "Environment"
        self._get_begin(envtype,nm,starred,env_options)
        self._get_end(envtype,starred,env_options)
        text_lines = text_lines if text_lines else []
        text_lines.insert(0,self.begin.get_as_line())
        text_lines.append(self.end.get_as_line())
        super().__init__(text_lines,nm)
        self._get_required_packages(required_packages)


    def get_required_packages(self):
        return self.required_packages

    # if position is None, appends to the end of the environment.
    # if it's an int, inserts at that position
    def add_interior_lines(self, new_text, position: int=None):
        p = len(self.lines)-1 if position is None else int(position)
        if isinstance(new_text,str):
            self.add_line(p,new_text)
        elif isinstance(new_text,Iterable):
            for i,ln in enumerate(new_text):
                self.add_line(p+i,ln)

    #adds a new line at the start of this Environment
    def prepend_line(self, new_line):
        self.add_line(1,new_line)

    def add_end_options_to_begin(self, new_opts):
        self.begin.add_end_options(new_opts)
        self.lines[0] = self.begin.get_as_line()
                
    def _get_required_packages(self, required_packages):
        self.required_packages = []
        if required_packages is None:
            return
        
        for pkg in required_packages:
            if isinstance(pkg,Command):
                if pkg not in self.required_packages:
                    self.required_packages.append(pkg)
            elif isinstance(pkg,str):
                if pkg not in self.required_packages:
                    self.required_packages.append(pkg)
            else:
                if pkg not in self.required_packages:
                    self.required_packages.append(UsePackage(*pkg))

        
    
    def _get_begin(self, envtype, name, starred, opts):
        if starred:
            self.begin = Command('begin',envtype+'*',opts)
        else:
            self.begin = Command('begin',envtype,opts)

    def _get_end(self, envtype, starred, opts):
        if starred:
            self.end = Command('end',envtype+'*')#,opts)
        else:
            self.end = Command('end',envtype)#,opts)

    def _set_begin(self, custom_begin):
        self.begin = custom_begin
        self.lines = self.lines[1:]
        self.lines[0] = self.begin if self.begin.endswith('\n') else self.begin+'\n'




class Equation(Environment):

    #__slots__ = ['ufl_handler']

    def __init__(self, math_text_lines: Iterable, starred: bool=False, eq_name: str=None):
        
        req_pkgs = [UsePackage('amsmath'),UsePackage('amsfonts')]
        super().__init__('equation',math_text_lines,eq_name if eq_name else 'Equation',
                         starred,env_options=None,required_packages=req_pkgs)

        #self.ufl_handler = None

    @staticmethod
    def from_ufl(ufl_expr, starred: bool=False, eq_name: str=None):
        """
        NOTE: variables that are usually called `u` and `v` (Functions) are all named w^i for some i. Those i values are usually pretty weird (e.g. if you only have two UFL Function variables in your code named u and v, you might get, say, a w^7 and a w^{10} in the PDF)
        """
        from ufl.formatting.ufl2unicode import ufl2unicode
        from pylatexenc.latexencode import unicode_to_latex
        uni = ufl2unicode(ufl_expr)
        uni = replace_superscripts(uni)
        uni = replace_subscripts(uni)
        code = unicode_to_latex(uni,unknown_char_policy='ignore')
        #could use a regex but that's just asking for bugs with so few cases
        #code = lines.replace('[i]','')#'_{i}')
        #code = code.replace('[i,i]','')#''_{ii}')
        #code = code.replace('[i,i,i]','')#''_{iii}')
        code = code.replace('\\ensuremath{\\forall} i,i','')
        code = code.replace('\\ensuremath{\\forall} i','')
        code = code.replace('{\\textasciicircum}','^')
        code = code.replace('{\\textunderscore}','_')
        code = code.replace('[rest of domain]','_{\\Omega}')
        code = code.replace('\\_','_')
        code = code.replace('\\{','{')
        code = code.replace('\\}','}')
        grad_pattern = '\ensuremath{\mathbf{g}}\ensuremath{\mathbf{r}}\ensuremath{\mathbf{a}}\ensuremath{\mathbf{d}}\\,'
        code = code.replace(grad_pattern,'\\nabla ')
        #grad(grad(x)) |--> div(grad(x))
        code = code.replace('\\nabla \\nabla ','\\nabla^2')
        #remove summation sign
        #code = code.replace('\ensuremath{\sum}','')
        return Equation([code],starred,eq_name)
        

class Section(TextLines):

    __slots__ = ['begin']
    
    def __init__(self, name: str, text_lines: Iterable, starred: bool=False, issubsection: bool = False):
        env = 'section*' if starred else 'section'
        if issubsection:
            env = 'sub'+env
        self.begin = Command(env,name if name else ' ',None)
        text_lines = text_lines if text_lines else []
        text_lines.insert(0,self.begin.get_as_line())
        super().__init__(text_lines,name if name else ' ')


class Subsection(Section):

    def __init__(self,name: str, text_lines: Iterable, starred: bool=False):
        super().__init__(name,text_lines,starred,issubsection=True)


