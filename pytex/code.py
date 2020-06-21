from .environment import Environment
from .command import Command, UsePackage, TextModifier
from .text import TextLines
from collections.abc import Iterable

def _comma_separated_tuple(tpl):
    n = len(tpl)
    csv = []
    for i,val in enumerate(tpl):
        if i < n-1:
            csv.append(str(val)+',')
        else:
            csv.append(str(val))

    return tuple(csv)                  


class CodeColor(TextLines):

    def __init__(self,name,values,color_scheme='rgb'):
        self._name = name
        self.vals = values
        self.color_scheme = color_scheme
        if self.vals:
            self._make_line()
            super().__init__([self.line],name)
        else:
            self._make_premade_color(name)
            super().__init__([self.line],name)
        

    def get(self):
        return self.line

    def get_as_line(self):
        return self.line if self.line.endswith('\n') else self.line + '\n'
    
    @staticmethod
    def Green():
        return CodeColor('green',(0,0.6,0),'rgb')

    @staticmethod
    def Gray():
        return CodeColor('gray',(0.0,0.5,0.5),'rgb')

    @staticmethod
    def Purple():
        return CodeColor('purple',(0.58,0,0.82),'rgb')

    @staticmethod
    def Magenta():
        return CodeColor('magenta',None)

    @staticmethod
    def Red():
        return CodeColor('red',None)

    @staticmethod
    def DefaultBackground():
        return CodeColor('PyTexDefaultBackground',(0.95,0.95,0.92),'rgb')
        
    def _make_line(self):
        self.line = '\\definecolor{' + self._name + '}{'
        for elem in _comma_separated_tuple(self.vals):
            self.line += elem
        self.line += '}\n'

    def _make_premade_color(self, pre_name):
        _PREMADE_XCOLORS = {'magenta','green','blue','red','brown'}
        if pre_name not in _PREMADE_XCOLORS:
            raise NotImplementedError(f"Cannot get premade xcolor {pre_name}! Premade colors are: {[x for x in _PREMADE_XCOLORS]}")
        self._name = pre_name
        self.vals = None
        self.color_scheme = 'rbg'
        self.line = None




class CodeStyle:

    def __init__(self, style_name: str,
                 background_color: CodeColor=CodeColor.DefaultBackground(),
                 comment_color: CodeColor=CodeColor.Green(),
                 keyword_color: CodeColor=CodeColor.Magenta(),
                 number_color: CodeColor=CodeColor.Gray(),
                 string_color: CodeColor=CodeColor.Red(),
                 basic_style_mods: Iterable=None,
                 whitespace_break: bool=False,
                 breaklines: bool=True,
                 caption_pos: str='b',
                 keep_spaces=True,
                 number_alignment='left',
                 number_sep_pts=5,
                 show_spaces=False,
                 show_string_spaces=False,
                 show_tabs=False,
                 tabsize=2):

        self._name = style_name
        self._get_style_options(background_color,comment_color,keyword_color,
                                number_color,string_color,basic_style_mods,
                                whitespace_break, breaklines, caption_pos,
                                keep_spaces, number_alignment, number_sep_pts,
                                show_spaces, show_string_spaces, show_tabs, tabsize)
        self._get_style_define()
        
        
    def get(self):
        return self.cmd

    def get_as_line(self):
        return self.cmd + '\n'

    def name(self):
        return self._name

    def command_to_set(self):
        return Command('lstset',[f'style={self._name}'])

    def _get_style_define(self):
        self.cmd = "\\lstdefinestyle{" + self._name + "}{\n"
        last_option = 'tabsize'
        n = len(self.options)
        i = 0
        for opt, val in self.options.items():
            if i < n - 1:
                self.cmd += opt + '=' + val + ',\n'
            else:
                self.cmd += opt + '=' + val + '\n'
            i += 1
        self.cmd += '}'



    def _get_style_options(self, background, comment, kw, num, string,
                           basic_style, whitespace, breaklines,
                           captionpos, keepspaces, numalign,
                           numseppts, showspaces, showstringspaces,
                           showtabs, tabsz):
        if basic_style is None:
            basic_style = [TextModifier('ttfamily'),TextModifier('footnotesize')]
            
        self.options = {'backgroundcolor' : '\\color{' + background.name() + '}',
                        'commentstyle' : '\\color{' + comment.name() + '}',
                        'keywordstyle' : '\\color{' + kw.name() + '}',
                        'numberstyle' : '\\color{' + num.name() + '}',
                        'stringstyle' : '\\color{' + string.name() + '}',
                        'basicstyle' : (basic_style.get() if isinstance(basic_style,str) else ''.join([x.get() for x in basic_style])),
                        'breaklines' : 'true' if breaklines else 'false',
                        'captionpos' : captionpos,
                        'keepspaces' : 'true' if keepspaces else 'false',
                        'numbers' : numalign,
                        'numbersep' : str(numseppts)+'pt',
                        'showspaces' : 'true' if showspaces else 'false',
                        'showstringspaces' : 'true' if showstringspaces else 'false',
                        'showtabs' : 'true' if showtabs else 'false',
                        'tabsize' : str(tabsz),
                        }
                        

_PYTEX_REQUIRED_CODE_PKGS = {
    ('listings',),
    ('xcolor',),
    ('inputenc',('utf8')),
    }


class CodeSnippet(Environment):

    def __init__(self, code_lines, language='C++', code_style=None, caption=None, name=None):
        self.style = code_style if code_style else CodeStyle('default_pytex_code_style')
        self.lang = language
        super().__init__('lstlisting',code_lines,
                         name if name else language + ' code snippet',False,self._listing_options(language,caption),
                         _PYTEX_REQUIRED_CODE_PKGS)
        self._get_style_use_cmd()
        #add the text stype as a required package to put it in the preamble
        self.required_packages.add(self.style.get_as_line())
        

    def _get_style_use_cmd(self):
        self.prepend_line(self.style.command_to_set().get_as_line())
        
    def _listing_options(self, lang, caption):
        if caption:
            return [f'language={lang}',f'caption={caption}']
        else:
            return [f'language={lang}']
