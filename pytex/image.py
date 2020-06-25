from collections.abc import Iterable
from .command import Command, UsePackage

class Image(Command):

    def __init__(self, path, scale: float=1.0, other_options: Iterable=None):
        self.path = path
        self.opts = None if (scale == 1.0 and (other_options is None)) else (['scale='+str(scale)] + ([x for x in other_options] if other_options else []))
        super().__init__('includegraphics',[self.path],self.opts)
        self.required_packages = [UsePackage('graphicx')]
        

        
