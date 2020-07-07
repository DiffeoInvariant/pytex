
def _format_line(string):
    s = str(string)
    if not s.endswith('\n'):
        s += '\n'
    return s

class TextLines:

    __slots__ = ['lines','_name','head_cmt']

    def __init__(self,lines,sec_name=None):
        self.lines = [_format_line(x) for x in lines] if lines else []
        self._name = str(sec_name) if sec_name else "PyTex TextLines section"
        self.head_cmt = _format_line(f"\n% {self.name()}")

    def __str__(self):
        return '\n'.join(self.lines)

    def __repr__(self):
        return self.__str__()

    def name(self):
        return self._name

    def get_lines(self):
        return self.lines

    def line_count(self):
        return len(self.lines)
    
    def add_line(self, pos: int, newline: str):
        self.lines.insert(pos,_format_line(newline))

    def prepend_line(self,new_line: str):
        self.lines.insert(0,new_line)

    def append_line(self,newline: str):
        self.lines.append(_format_line(newline))

    def write(self,open_file):
        open_file.write(self.head_cmt)
        for ln in self.lines:
            open_file.write(ln)

            
