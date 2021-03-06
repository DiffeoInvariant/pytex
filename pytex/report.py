from pytex import Document, Environment, Command, TextModifier, Section, Subsection, CodeColor, CodeStyle, CodeSnippet, Image, Figure
from pytex.utils import register_colors, view_registered_colors, remove_colors
from collections.abc import Iterable
from inspect import getsource, getsourcelines
import subprocess

def make_pytest_report(pytest_output_file, **kwargs):
    ofile = open(pytest_output_file,'r')
    clean_lines = []
    for line in ofile.readlines():
        #print(line.encode('ascii'),'\n')
        print("split line:",line.encode('ascii').split(b'\x1b['))
        register_colors(line,['blue','green','red'])
        print(f"line without color defs: {remove_colors(line)}")
        line = remove_colors(line)
        #print("colors:\n")
    view_registered_colors()







class TestReport(Document):

    def __init__(self, filename: str, report_title: str=None, author: str=None, use_date: bool=False, **kwargs):
        report_title = report_title if report_title else 'PyTeX-Generated Test Report'
        super().__init__(filename, title=report_title,author=author,use_date=use_date,**kwargs)
        # pass in code_colors as a dictionary mapping
        # any (or multiple) of the strings {background_color,comment_color,keyword_color,number_color,string_color} or the Iterable[str] basic_style_mods
        # to instances of pytex.CodeColor
        self.custom_code_colors = kwargs.get('code_colors',None)
        self._get_code_style()


    def add_code_snippet(self, code_lines: Iterable, language='C++', caption=None, xleftmargin=None, xrightmargin=None):
        self.append(CodeSnippet(code_lines,language=language,code_style=self.code_style,caption=caption,xleftmargin=xleftmargin,xrightmargin=xrightmargin))

    def add_python_function(self, func, caption=None):
        try:
            lines = getsourcelines(func)[0]
            self.add_code_snippet(lines,language='Python',caption=caption)
            
        except OSError as exc:
            print(f"Error, could not find source code for function {func}!")
            raise

    def add_python_object(self, obj, caption=None):
        try:
            lines = getsourcelines(obj)[0]
            self.add_code_snippet(lines,language='Python',caption=caption)
            
        except OSError as exc:
            print(f"Error, could not find source code for object {obj}!")
            raise
        

    #def add_pytest_header(self, header_lines


    def add_section(self, section_name: str, text_lines: Iterable):
        self.append(Section(section_name,text_lines))

    def add_subsection(self, section_name: str, text_lines: Iterable):
        self.append(Subsection(section_name, text_lines))

    def add_image(self, path: str, scale: float=1.0, other_options=None):
        if ('h' in other_options or 'H' in other_options or 'H!' in other_options):
            self.append(Figure(Image(path,scale),other_options))
        else:
            self.append(Image(path,scale,other_options))
        
    def _get_code_style(self):
        styles = {'background_color' : CodeColor.DefaultBackground(),
                  'comment_color' : CodeColor.Green(),
                  'keyword_color' : CodeColor.Magenta(),
                  'number_color' : CodeColor.Gray(),
                  'string_color' : CodeColor.Red(),
                  'basic_style_mods' : None}

        if self.custom_code_colors:
            for k in self.custom_code_colors.keys():
                if k in styles.keys():
                    styles[k] = self.custom_code_colors[k]

        self.code_style = CodeStyle('ReportStyle',**styles)

        
        
        


    
