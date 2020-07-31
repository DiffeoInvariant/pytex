from typing import List

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
        self.head_cmt = _format_line(f"% {self.name()}")

    def __str__(self):
        return '\n'.join(self.lines)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_file(filename: str):
        lines = [line for line in open(filename,'r')]
        name = filename
        if lines[0].startswith('% '):
            name = lines[0].split('% ')[1]
            lines = lines[1:]
        return TextLines(lines,name)


    def name(self) -> str:
        return self._name

    def get_lines(self) -> List[str]:
        return self.lines

    def line_count(self) -> int:
        return len(self.lines)

    def __len__(self):
        return len(self.lines)

    def __iter__(self):
        for line in self.lines:
            yield line

    
    def add_line(self, pos: int, newline: str) -> None:
        self.lines.insert(pos,_format_line(newline))

    def prepend_line(self,new_line: str) -> None:
        self.lines.insert(0,new_line)

    def append_line(self,newline: str) -> None:
        self.lines.append(_format_line(newline))

    def append_lines(self, new_lines) -> None:
        for line in new_lines:
            self.append_line(line)

    def write(self,open_file) -> None:
        open_file.write(self.head_cmt)
        for ln in self.lines:
            open_file.write(ln)


    def save(self, filename) -> None:
        try:
            with open(filename,'w') as f:
                self.write(f)
        except:
            raise

            
            
