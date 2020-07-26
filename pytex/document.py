from .command import Command, UsePackage, TextModifier
from .text import TextLines
from .code import CodeStyle
from .environment import Environment
from collections.abc import Iterable
from os.path import abspath, exists, dirname
from os import makedirs
import subprocess
from pickle import Pickler, Unpickler, dump, load

class DocumentClass(Command):

    __slots__ = ['fontsz']

    def __init__(self,font_pts=11,document_type='article',other_options=None):
        self.fontsz = str(font_pts)+'pt'
        if other_options:
            opts = other_options.insert(0,self.fontsz)
        else:
            opts = [self.fontsz]

        super().__init__('documentclass',args=[document_type],options=opts)
        

def article_class(font_pts=11,other_options=None):
    return DocumentClass(font_pts,'article',other_options)



        
class Preamble(TextLines):

    __slots__ = ['packages','title','author','date','make_title_command','title_data_commands']
    '''
    Args:
    doc_class: a DocumentClass object
     use_packages: list/tuple of tuples of (package_name,package_options)
    (package_options can be either list/tuple or None)
    '''
    def __init__(self, doc_class: DocumentClass, use_packages: Iterable, title: str=None, author: str=None, use_date:bool = False):
        self.packages = list(use_packages)
        lines = [doc_class.get_as_line(),'\n']
        for package in use_packages:
            if isinstance(package,UsePackage):
                lines.append(package.get_as_line())
            elif isinstance(package,CodeStyle):
                lines.append(package.get_as_line())
            elif isinstance(package,str):
                lines.append(package)
            else:
                lines.append(UsePackage(*package).get_as_line())


        super().__init__(lines,"Preamble for pytex-generated document")
        self._make_title(title,author,use_date)

    def title_data(self):
        return self.title_data_commands

    def make_title(self):
        return self.make_title_command


    def set_title(self, title, author=None, use_date=False):
        self._make_title(title,author,use_date)

    def _make_title(self, title, author, use_date):
        self.title = Command('title',[title]) if title else None
        self.author = Command('author',[author]) if author else None
        self.date = Command('date{}',None) if not use_date else None
        self.title_data_commands = [self.title,self.author,self.date]

        for cmd in self.title_data_commands:
            if cmd:
                self.append_line(cmd.get_as_line())
        self.make_title_command = TextModifier('maketitle') if (title or author or use_date) else None
                              





class Document(Environment):

    __slots__ = ['sections','environments','preamble','title',
                 'author','use_date','iswritten','doc_class','pickler']
    def __init__(self, filename: str, **kwargs):
        super().__init__('document',None,
                         name=self._format_filename(filename),starred=False)

        
        #list of TextLines (or derived) instances that make up this Document
        self.sections = []
        self.environments = []
        self.preamble = None
        self.title = kwargs.get('title',None)
        self.author = kwargs.get('author',None)
        self.use_date = kwargs.get('use_date',False)
        self.iswritten = False
        self._get_doc_class(**kwargs)
        self.pickler = None
        
    def add_required_packages(self, pkgs):
        if isinstance(pkgs, Environment):
            reqs = pkgs.get_required_packages()
        else:
            reqs = []
            for pkg in pkgs:
                if isinstance(pkg,UsePackage):
                    if pkg not in reqs:
                        reqs.append(pkg)
                elif isinstance(pkg,CodeStyle):
                    for coldef in pkg.color_definitions():
                        if coldef not in reqs:
                            reqs.append(coldef)
                    if pkg not in reqs:
                        reqs.append(pkg)
                elif isinstance(pkg,Iterable):
                    reqs.append(UsePackage(*pkg))
                else:
                    reqs.append(UsePackage(pkg))
                    
        for pkg in reqs:
            if pkg not in self.required_packages:
                self.required_packages.append(pkg)


    def add(self, new_text: Iterable):
        for item in new_text:
            self.append(item)
            
    # takes a TextLines, Environment or derived
    def append(self, new_text):
        self.sections.append(new_text)
        if isinstance(new_text, Environment):
            self.environments.append(new_text)
        else:
            self.environments.append(None)
        

    def insert(self, pos: int, new_text):
        try:
            self.sections.insert(pos,new_lines)
            if isinstance(new_text, Environment):
                self.environments.insert(pos,new_text)
            else:
                self.environments.insert(pos,None)
        except:
            raise


    def serialize(self, filename: str=None):
        if filename is None:
            filename = 'document.dat'
        dump(self,open(filename,'wb'))

    @staticmethod
    def from_file(filename: str):
        with open(filename,'rb') as fnm:
            return load(fnm)


    def _get_doc_class(self, **kwargs):
        self.doc_class = kwargs.get('doc_class',None)
        if self.doc_class is None:
            self.doc_class = kwargs.get('document_class',DocumentClass())

        self.doc_class

    def _set_required_packages(self):
        #NOTE: call right before writing
        for env in self.environments:
            if env:
                self.add_required_packages(env)


    def _make_preamble(self):
        self._set_required_packages()
        self.preamble = Preamble(self.doc_class,self.required_packages,self.title,self.author,self.use_date)


    def set_title(self, title, author=None, use_date=False):
        self.title = title
        if author and author != self.author:
            self.author = author

        if use_date and use_date != self.use_date:
            self.use_date = use_date

    def set_author(self,author=None):
        self.author = author

    def set_use_date(self,use_date=True):
        self.use_date = use_date
        


    def __str__(self):
        self._set_required_packages()
        prbl = Preamble(self.doc_class,self.required_packages,self.title,self.author,self.use_date)
        strep = str(prbl)

        strep += self.begin.get_as_line()
        if prbl.make_title():
            strep += self.preamble.make_title().get_as_line()

        for sec in self.sections:
            strep += str(sec)

        strep += self.end.get_as_line()

        return strep
        
    def write(self):
        self._make_preamble()
        with open(self.name(),'w') as f:
            self._ensure_directory_exists()
            self.preamble.write(f)
            f.write(self.begin.get_as_line())
            if self.preamble.make_title():
                f.write(self.preamble.make_title().get_as_line())
            f.write('\n')
            for sec in self.sections:
                sec.write(f)

            f.write('\n')
            f.write(self.end.get_as_line())
            
        self.iswritten = True
        
    def compile(self):
        if not self.iswritten:
            self.write()

        compile_cmds = ['pdflatex', self.name()]
        
        outputs = subprocess.run(compile_cmds, capture_output=True)
        return outputs

    def _ensure_directory_exists(self):
        drct = dirname(abspath(self.name()))
        if not exists(drct):
            makedirs(drct)
        
    @staticmethod
    def _format_filename(filename):
        return abspath(filename) if filename.endswith('.tex') else abspath(filename + '.tex')

            
        
