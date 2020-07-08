from .text import TextLines
from .command import Command, UsePackage
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

    #adds a new line BEFORE the start of this Environment
    def prepend_line(self, new_line):
        self.add_line(0,new_line)

    def add_end_options_to_begin(self, new_opts):
        self.begin.add_end_options(new_opts)
                
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


