import pytest
#from pytest.config import Config
#from pytest.config import create_terminal_writer
#from pytest.config.argparsing import Parser
#from pytest.terminal import TerminalReporter
#from pytest.store import StoreKey
import pytex
from typing import IO
from tempfile import TemporaryFile,NamedTemporaryFile
import shutil

#going based off code at https://github.com/pytest-dev/pytest/blob/master/src/_pytest/pastebin.py

pytexfile_key = 'ptfkey'#StoreKey[IO[bytes]]()

@pytest.hookimpl(tryfirst=True)
def pytest_addoption(parser) -> None:
    group = parser.getgroup("terminal reporting")
    group._addoption(
        "--pytex_file",
        metavar="mode",
        action="store",
        dest="pytex_file",
        default=None,
        help="Turn output into a PyTeX TestReport",
        )
    



@pytest.hookimpl(trylast=True)
def pytest_configure(config) -> None:
    if config.option.pytex_file:
        #get a terminal writer, intercept strings on the way to the terminal, store them in a file, and if not in fileonly mode, print to the terminal
        tr = config.pluginmanager.getplugin("terminalreporter")
        if tr:
            config._store[pytexfile_key] = open(config.option.pytex_file,'w+b')
            oldwrite = tr._tw.write
            
            def new_write(s, **kwargs):
                if config.option.pytex_file:
                    oldwrite(s,**kwargs)
                if isinstance(s,str):
                    s = s.encode('utf-8')
                config._store[pytexfile_key].write(s)

            tr._tw.write = new_write


def pytest_unconfigure(config) -> None:
    if pytexfile_key in config._store:
        pytexfile = config._store[pytexfile_key]
        #pytex_dest = config.option.pytex_file
        #shutil.copyfile(pytexfile.name,config.option.pytex_file)
        pytexfile.close()
        pytex.make_pytest_report(config.option.pytex_file)
        #undo the modifications to the terminal reporter in pytest_configure()
        tr = config.pluginmanager.getplugin('terminalreporter')
        del tr._tw.__dict__['write']
        
        


    
    
        
