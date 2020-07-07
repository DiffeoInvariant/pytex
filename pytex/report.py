from pytex import Document, Environment, Command, TextModifier, Section, Subsection, CodeColor, CodeStyle, CodeSnippet, Image
from collections.abc import Iterable
from inspect import getsource, getsourcelines

class TestReport(Document):

    def __init__(self, filename: str, report_title: str=None, author: str=None, use_date: bool=False, **kwargs):
        report_title = report_title if report_title else 'PyTeX-Generated Test Report'
        super().__init__(filename, title=report_title,author=author,use_date=use_date)
        # pass in code_colors as a dictionary mapping
        # any (or multiple) of the strings {background_color,comment_color,keyword_color,number_color,string_color} or the Iterable[str] basic_style_mods
        # to instances of pytex.CodeColor
        self.custom_code_colors = kwargs.get('code_colors',None)
        self._get_code_style()


    def add_code_snippet(self, code_lines: Iterable, language='C++', caption=None):
        self.append(CodeSnippet(code_lines,language=language,code_style=self.code_style,caption=caption))

    def add_python_function(self, func, caption=None):
        try:
            lines = getsourcelines(func)[0]
            self.add_code_snippet(lines,language='Python',caption=caption)
            
        except OSError as exc:
            print(f"Error, could not find source code for function {func}!")
            raise
        
        


    def add_section(self, section_name: str, text_lines: Iterable):
        self.append(Section(section_name,text_lines))

    def add_subsection(self, section_name: str, text_lines: Iterable):
        self.append(Subsection(section_name, text_lines))

    def add_image(self, path: str, scale: float=1.0, other_options=None):
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

        
        
        


    
