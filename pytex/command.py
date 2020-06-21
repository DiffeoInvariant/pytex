from collections.abc import Iterable

class Command:

    def __init__(self,cmd,args=None,options=None):
        self.cmd = '\\' + cmd
        self._get_args(args)
        self._get_options(options)
        self._build_command()


    # constructs a Command from a tuple of (command_name,options,args) (options and/or args can be None)

    @staticmethod
    def from_tuple(name_opts_args):
        if len(name_opts_args) >= 3:
            return Command(name_opts_args[0],name_opts_args[1],name_opts_args[2])
        elif len(name_opts_args) >= 2:
            return Command(name_opts_args[0],name_opts_args[1],None)
        else:
            return Command(name_opts_args[0],None,None)
    
    def get(self):
        return self.cmd


    def __str__(self):
        return self.cmd

    def __repr__(self):
        return self.cmd

    def get_options(self):
        return self.options

    def get_args(self):
        return self.args

    def get_as_line(self):
        return self.cmd + '\n'

    def write(self,open_file):
        open_file.write(self.cmd)

    def write_line(self,open_file):
        open_file.write(self.get_as_line())

    

    def _build_string(self,base,lst,left_char='{',right_char='}'):
        res = base
        if left_char:
         res += str(left_char)

        n = len(lst)
        for i,l in enumerate(lst):
            if i < n-1:
                res += l + ', '
            else:
                res += l

        if right_char:
            res += str(right_char)

        return res
        
    def _build_command(self):
        if self.opts:
            self.cmd = self._build_string(self.cmd,self.opts,'[',']')
        if self.args:
            self.cmd = self._build_string(self.cmd,self.args,'{','}')


    def _get_args(self,args):
        if isinstance(args,str):
            self.args = [x.strip() for x in args.split(",")]
        elif args:
            self.args = [str(x) for x in args]
        else:
            self.args = args

    def _get_options(self,options):
        if isinstance(options,str):
            self.opts = [x.strip() for x in options.split(",")]
        elif options:
            self.opts = [str(x) for x in options]
        else:
            self.opts = options
            

class UsePackage(Command):
    def __init__(self,package_name,package_options=None):
        super().__init__('usepackage',args=str(package_name),options=package_options)


class NewCommand:

    def __init__(self,new_command_name: str, new_command_replaces: str, num_args: int=0, defaults=None):
        self.decl = '\newcommand{' + new_command_name + '}'
        if int(num_args) > 0:
            self.decl += str('[' + str(num_args) + ']')
        if defaults:
            if isinstance(defaults,str):
                self.decl += str('[' + defaults + ']')
            elif isinstance(defaults,Iterable):
                self.decl += '['
                for df in defaults:
                    self.decl += str(df) + ', '
                self.decl += ']'

        self.decl += str('{' + new_command_replaces + '}')

    def get_as_line(self):
        return self.decl + '\n' if not self.decl.endswith('\n') else self.decl

    def get(self):
        return self.decl

    def write(self,open_file):
        open_file.write(self.decl)

    def write_as_line(self,open_file):
        open_file.write(self.get_as_line())
            



class TextModifier(Command):

    def __init__(self,cmd):
        super().__init__(cmd,None,None)
