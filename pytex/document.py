from .command import Command, UsePackage
from .text import TextLines
from .code import CodeStyle
from .environment import Environment
from collections.abc import Iterable
from os.path import abspath

class DocumentClass(Command):

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

    '''
    Args:
    doc_class: a DocumentClass object
     use_packages: list/tuple of tuples of (package_name,package_options)
    (package_options can be either list/tuple or None)
    '''
    def __init__(self, doc_class: DocumentClass, use_packages: Iterable):
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





class Document(Environment):

    def __init__(self, filename: str, **kwargs):
        super().__init__('document',None,
                         name=self._format_filename(filename),starred=False)

        
        #list of TextLines (or derived) instances that make up this Document
        self.sections = []
        self.environments = []
        self.preamble = None
        self._get_doc_class(**kwargs)
        
    def add_required_packages(self, pkgs):
        if isinstance(pkgs, Environment):
            reqs = pkgs.get_required_packages()
        else:
            reqs = set({})
            for pkg in pkgs:
                if isinstance(pkg,UsePackage):
                    reqs.add(pkg)
                elif isinstance(pkg,CodeStyle):
                    reqs.add(pkg)
                elif isinstance(pkg,Iterable):
                    reqs.add(UsePackage(*pkg))
                else:
                    reqs.add(UsePackage(pkg))
                    
        for pkg in reqs:
            self.required_packages.add(pkg)


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
        self.preamble = Preamble(self.doc_class,self.required_packages)


    def write(self):
        self._make_preamble()
        with open(self.name(),'w') as f:
            self.preamble.write(f)
            f.write(self.begin.get_as_line())
            f.write('\n')
            for sec in self.sections:
                sec.write(f)

            f.write('\n')
            f.write(self.end.get_as_line())
        
        
    @staticmethod
    def _format_filename(filename):
        return abspath(filename) if filename.endswith('.tex') else abspath(filename + '.tex')

            
        
